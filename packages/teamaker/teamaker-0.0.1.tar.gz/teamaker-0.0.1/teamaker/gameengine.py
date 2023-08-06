#!/usr/bin/python
# Standard libraries
from functools import wraps
from itertools import combinations
from typing import Any, Callable, Union, NewType
from typing import List, Dict, Set, Tuple, Iterable
import ast
import importlib
import itertools
import json
import logging
import os
import pickle
import re
import sys
import tempfile
import time

# Third-party libraries
import cerberus  # type: ignore
from overrides import overrides, EnforceOverrides, final
from watchdog.events import FileSystemEvent, FileSystemEventHandler  # type: ignore
from watchdog.observers import Observer  # type: ignore

# Our own libraries

# Type hint aliases
Key = NewType('Key', str)
SceneName = Key
TransitionCondition = NewType('TransitionCondition', str)
Scene = Dict[str, Any]
Scenes = Dict[SceneName, Scene]
Commands = Dict[str, Tuple[str, Callable[[str], str]]]
Actions = List[Tuple[Callable[[str], bool], Callable[[str], str]]]
Transition = Union[SceneName, Tuple[TransitionCondition, SceneName, SceneName]]
Switch = Union[Tuple[Key, str], Tuple[Key, str, str]]
ConditionalOperatorCallbacks = Dict[str, Callable[[Key], bool]]
GraphNode = Dict[str, Any]
Graph = Dict[str, GraphNode]
CONDITION_OPERAND_START = '['
CONDITION_OPERAND_END = ']'
CONDITION_OPERATOR_HAS = 'has'
CONDITION_OPERATOR_IS = 'is'
DEFAULT_TRANSITION = ''

# Should not contain brackets: reserved for conditions, e.g. has[red key]
KEY_REGEX = r'[a-zA-Z0-9 _,\.-:\(\)]*'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Story file schema (used for Cerberus validation)
string_schema = {
    'type': 'string'
}

key_schema = {
    'type': 'string',
    'regex': KEY_REGEX,
}

scene_name_schema = key_schema

conditional_schema = {
    'items': [
        # [condition, condition_true_transition, condition_false_transition]
        string_schema,
        scene_name_schema,
        scene_name_schema,
    ]
}

transition_schema = {
    'anyof': [
        scene_name_schema,
        conditional_schema,
    ]
}

switch_schema = {
    'anyof': [
        {
            # [switch_name, turn_switch_on_message]
            'items': [
                key_schema,
                string_schema,
            ],
        },
        {
            # [switch_name, turn_switch_on_message, turn_switch_off_message]
            'items': [
                key_schema,
                string_schema,
                string_schema,
            ]
        }
    ]
}

story_schema: Dict = {
    'start_scene': string_schema,
    'scenes': {
        'type': 'dict',
        'keysrules': key_schema,
        'valuesrules': {
            'schema': {
                'text': {
                    'type': 'string',
                    'required': True,
                },
                'transitions': {
                    'type': 'dict',
                    'keysrules': key_schema,
                    'valuesrules': transition_schema,
                    'required': True,
                },
                'items': {
                    'type': 'dict',
                    'keysrules': key_schema,
                    'valuesrules': {
                        'items': [
                            key_schema,
                            string_schema,
                        ],
                    },
                },
                'descriptions': {
                    'type': 'dict',
                    'keysrules': key_schema,
                    'valuesrules': string_schema,
                },
                'switches': {
                    'type': 'dict',
                    'keysrules': key_schema,
                    'valuesrules': switch_schema,
                },
            },
        },
    },
}


def unique_sorted_list(objects: Iterable) -> List:
    return sorted(list(set(objects)))


def import_optional_module(module_name: str, package: str) -> Any:
    if module_name in globals():
        module = globals()[module_name]
    else:
        try:
            module = importlib.import_module(module_name)
            globals()[module_name] = module
        except ModuleNotFoundError:
            logging.error(f'{module_name} package is required but not installed.')
            logging.error(f'You can install it with: pip install {package}')
            sys.exit(1)

    return module


def is_transition_conditional(transition: Transition) -> bool:
    assert isinstance(transition, str) or \
        isinstance(transition, list) and len(transition) == 3, f'Invalid transition: {transition}'
    return isinstance(transition, list)


def split_transition_to_condition_and_scenes(transition: Transition) -> Tuple[TransitionCondition, SceneName, SceneName]:
    assert is_transition_conditional(transition), transition
    return TransitionCondition(transition[0]), SceneName(transition[1]), SceneName(transition[2])


def create_transition_graph(scenes: Scenes) -> Graph:
    graph = {}
    for scene in scenes.values():
        graph[scene['name']] = {
            'name': scene['name'],
            'type': 'normal',
            'outgoing': set(),
            'text': scene['text'],
        }

    for scene in scenes.values():
        source_scene = scene['name']
        for key, transition in scene['transitions'].items():
            if is_transition_conditional(transition):
                condition, true_scene, false_scene = split_transition_to_condition_and_scenes(transition)

                graph[condition] = {
                    'name': condition,
                    'type': 'condition',
                    'outgoing': set(),
                    'text': '',
                }
                graph[source_scene]['outgoing'].add((condition, key))
                graph[condition]['outgoing'].add((true_scene, 'yes'))
                graph[condition]['outgoing'].add((false_scene, 'no'))
            else:
                destination_scene = transition
                graph[source_scene]['outgoing'].add((destination_scene, key))

    for node in graph.values():
        node['outgoing'] = unique_sorted_list(node['outgoing'])

    return graph


def visit_all_reachable_nodes(node: Scene, graph: Dict, visited_nodes: Set[SceneName], callback: Callable[[GraphNode], None] = None) -> None:
    if node['name'] not in visited_nodes:
        if callback:
            callback(node)
        visited_nodes.add(node['name'])
        for name, _ in node['outgoing']:
            visit_all_reachable_nodes(graph[name], graph, visited_nodes, callback)


def visit_all_nodes(graph: Graph, callback: Callable[[GraphNode], None]) -> None:
    all_nodes = set(graph.keys())
    reachable_nodes = set()  # type: Set[SceneName]
    while len(reachable_nodes) != len(all_nodes):
        non_visited_nodes = unique_sorted_list(all_nodes.difference(reachable_nodes))
        visit_all_reachable_nodes(graph[non_visited_nodes[0]], graph, reachable_nodes, callback)


def print_transition_graph_to_file(scenes_file_path: str) -> None:
    graphviz = import_optional_module('graphviz', 'graphviz')

    def print_node(node: GraphNode, dot) -> None:
        is_normal_node = node['type'] == 'normal'
        assert is_normal_node or node['type'] == 'condition'
        dot.node(node['name'],
                 tooltip=f"\"{node['text']}\"" if is_normal_node else "",
                 fontsize='14',
                 fontname='helvetica-bold' if is_normal_node else 'helvetica',
                 fontcolor='#cc2222' if is_normal_node else '#cc22cc',
                 shape='note' if is_normal_node else 'rectangle',
                 color='#999999',
                 style='filled', fillcolor='#eeeeee')
        for outgoing, key in node['outgoing']:
            dot.edge(node['name'], outgoing, label=key,
                     tooltip=f"{node['name']} -> [{key}] -> {outgoing}",
                     fontsize='14',
                     fontname='helvetica',
                     fontcolor='#33aa33',
                     color='#555555')

    scenes, _ = StoryLoader().load_story(scenes_file_path)
    graph = create_transition_graph(scenes)

    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', tooltip=' ')  # concentrate='true'
    visit_all_nodes(graph, lambda graph_node: print_node(graph_node, dot))
    source_filename = 'transitions.txt'
    svg_filename = dot.render(source_filename, format='svg')
    logging.info(f'Transition graph saved to files {source_filename}, {svg_filename}')


class StoryLoader:
    def load_story(self, scenes_file_path: str) -> Tuple[Scenes, SceneName]:
        scene_loader_for_extension = {
            'py': self._load_story_from_py,
            'yaml': self._load_story_from_yaml,
        }

        extension = scenes_file_path.split('.')[-1]
        if extension not in scene_loader_for_extension:
            logging.error(f'Unsupported story file extension: {extension}. Supported extensions: {list(scene_loader_for_extension.keys())}')
            sys.exit(1)

        story = scene_loader_for_extension[extension](scenes_file_path)
        self._validate_scenes_schema(story)

        scenes = story['scenes']  # type: Scenes
        start_scene = story['start_scene']  # type: SceneName
        self._initialize_scenes_optional_fields(scenes)

        return scenes, start_scene

    def _load_story_from_py(self, scenes_file_path: str) -> Dict:
        return ast.literal_eval(open(scenes_file_path).read())

    def _load_story_from_yaml(self, scenes_file_path: str) -> Dict:
        yaml = import_optional_module('yaml', 'PyYAML')

        return yaml.safe_load(open(scenes_file_path))

    def _validate_scenes_schema(self, story: Dict) -> None:
        v = cerberus.Validator()
        assert v.validate(story, story_schema), json.dumps(v.errors, indent=4)

    def _initialize_scenes_optional_fields(self, scenes: Scenes) -> None:
        scene_schema = story_schema['scenes']['valuesrules']['schema']
        scene_optional_fields = [(k, v['type']) for k, v in scene_schema.items() if 'required' not in v or not v['required']]
        for scene_name, scene in scenes.items():
            scene['name'] = scene_name
            for field, field_type in scene_optional_fields:
                if field not in scene:
                    scene[field] = eval(field_type)()


class SceneChecker:
    def check_scenes(self, scenes: Scenes, start_scene: SceneName,
                     commands: List[str]) -> None:
        self._check_scenes_correctness(scenes, commands)
        graph = create_transition_graph(scenes)
        self._check_scenes_reachability(graph, start_scene)

    def _get_scene_names_from_transition(self, transition: Transition) -> List[SceneName]:
        if is_transition_conditional(transition):
            _, true_scene, false_scene = split_transition_to_condition_and_scenes(transition)
            scene_names = [true_scene, false_scene]
        else:
            scene_names = [SceneName(str(transition))]

        return scene_names

    def _check_scenes_correctness(self, scenes: Scenes, commands: List[str]) -> None:
        for scene_name, scene in scenes.items():
            assert re.match(r'^%s$' % KEY_REGEX, scene_name), f'Scene "{scene_name}": invalid scene name'

            get_keys = lambda scene, key_type: list([k for k in scene[key_type].keys() if k != DEFAULT_TRANSITION])
            keys = [
                ('transition', get_keys(scene, 'transitions')),
                ('description', get_keys(scene, 'descriptions')),
                ('item', get_keys(scene, 'items')),
                ('switch', get_keys(scene, 'switches')),
            ]
            self._check_scene_keys_correctness(scene_name, commands, keys)
            self._check_bracketed_words_are_keys(scene_name, scene['text'], list(itertools.chain.from_iterable([key_list for _, key_list in keys])))
            self._check_scene_transitions(scene, scenes)

    def _check_scene_keys_correctness(self, scene_name: SceneName, commands: List[str], keys: List[Tuple[str, List[Key]]]) -> None:
        self._check_scene_keys_are_unique_within_scene(scene_name, keys)
        self._check_scene_keys_do_not_conflict_with_reserved_commands(scene_name, commands, keys)

    def _check_scene_keys_are_unique_within_scene(self, scene_name: SceneName, keys: List[Tuple[str, List[Key]]]) -> None:
        for (key_type1, key_list1), (key_type2, key_list2) in combinations(keys, 2):
            for key1 in key_list1:
                assert key1 not in key_list2, f'Scene "{scene_name}": {key_type1} key "{key1}" is also {key_type2} key'
                for key2 in [k for k in key_list1 if k != key1]:
                    assert not key1.endswith(key2) and not key2.endswith(key1), f'Scene "{scene_name}": {key_type1} keys "{key1}" and "{key2}" overlap'
                for key2 in key_list2:
                    assert not key1.endswith(key2) and not key2.endswith(key1), f'Scene "{scene_name}": {key_type1} key "{key1}" and {key_type2} key "{key2}" overlap'

    def _check_scene_keys_do_not_conflict_with_reserved_commands(self, scene_name: SceneName, commands: List[str], keys: List[Tuple[str, List[Key]]]) -> None:
        for (key_type, key_list) in keys:
            for key in key_list:
                assert re.match(r'^%s$' % KEY_REGEX, key), f'Scene "{scene_name}": {key_type} key "{key}" has invalid name'
                assert key not in commands, f'Scene "{scene_name}": {key_type} key "{key}" is a reserved command'
                for command in commands:
                    assert not key.endswith(command), f'Scene "{scene_name}": {key_type} key "{key}" ends with reserved command "{command}"'

    def _check_bracketed_words_are_keys(self, scene_name: SceneName, text: str, key_names: List[Key]) -> None:
        bracketed_words_regex = r'\[(%s)\]' % KEY_REGEX
        for bracketed_word in re.findall(bracketed_words_regex, text):
            assert bracketed_word in key_names, f'Scene "{scene_name}": no key for bracket word "{bracketed_word}"'

        for key_name in key_names:
            if '[%s]' % key_name not in text:
                logging.warning(f'Scene "{scene_name}": no bracketed word in text for key "{key_name}" (ignore if intended)')

    def _check_scene_transitions(self, scene: Scene, scenes: Scenes) -> None:
        scene_name = scene['name']
        for key, transition in scene['transitions'].items():
            for transition_scene in self._get_scene_names_from_transition(transition):
                assert transition_scene in scenes, f'Scene "{scene_name}": transition scene "{transition_scene}" does not exist'

    def _check_scenes_reachability(self, graph: Dict, start_scene: SceneName) -> None:
        assert start_scene in graph, f'Start scene "{start_scene}" not found in scenes'
        unreachable_nodes = self._get_unreachable_nodes(graph, start_scene)
        if unreachable_nodes:
            logging.warning('Unreachable scenes (no path from start scene): [%s]' % ', '.join(sorted(unreachable_nodes)))

    def _get_unreachable_nodes(self, graph: Dict, start_scene: SceneName) -> List:
        all_nodes = set(graph.keys())
        start_node = graph[start_scene]
        reachable_nodes = set()  # type: Set[SceneName]
        visit_all_reachable_nodes(start_node, graph, reachable_nodes)

        return sorted(all_nodes.difference(reachable_nodes))


class StateManager(EnforceOverrides):
    def __init__(self) -> None:
        self._state = {}  # type: Dict[str, Any]

    def initialize(self) -> None:
        self._set('scenes_visited', [])
        self._set('popup_shown', False)
        self._set('inventory', {})
        self._set('switches', {})

    def append_scene_visited(self, scene: Scene) -> None:
        self._set('scenes_visited', self._get('scenes_visited') + [scene])

    def get_scenes_visited(self) -> List[Dict]:
        return self._get('scenes_visited')

    def get_current_scene(self) -> Dict:
        return self.get_scenes_visited()[-1]

    def set_popup_shown(self, state: bool) -> None:
        self._set('popup_shown', state)

    def is_popup_shown(self) -> bool:
        return self._get('popup_shown')

    def add_to_inventory(self, item: str, description: str) -> None:
        inventory = self._get('inventory')
        inventory[item] = description
        self._set('inventory', inventory)

    def is_in_inventory(self, item: str) -> bool:
        return item in self.get_inventory()

    def get_inventory(self) -> Dict[str, str]:
        return self._get('inventory')

    def set_switch(self, name: str, value: bool) -> None:
        switches = self._get('switches')
        switches[name] = value
        self._set('switches', switches)

    def toggle_switch(self, name: str) -> None:
        self.set_switch(name, not self.is_switch_on(name))

    def is_switch_on(self, name: str) -> bool:
        switches = self._get('switches')
        return switches[name] if name in switches else False

    def _set(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def _get(self, key: str) -> Any:
        raise NotImplementedError


class MemoryStateManager(StateManager):
    def __init__(self) -> None:
        super().__init__()
        self._state = {}  # type: Dict[str, Any]

    @overrides
    def _set(self, key: str, value: Any) -> None:
        self._state[key] = value

    @overrides
    def _get(self, key: str) -> Any:
        return self._state[key]


class RedisStateManager(StateManager):
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT) -> None:
        super().__init__()
        self._redis = self._connect(host, port)

    def _connect(self, host: str, port: int) -> Any:
        redis = import_optional_module('redis', 'redis')

        client = redis.Redis(host=host, port=port)
        try:
            client.ping()
        except redis.exceptions.ConnectionError as e:
            logging.error(f'Redis: {e}')
            sys.exit(1)
        logging.info(f'Redis client: {host}:{port}')

        return client

    @overrides
    def _set(self, key: str, value: Any) -> None:
        ok = self._redis.set(key, pickle.dumps(value))
        assert ok

    @overrides
    def _get(self, key: str) -> Any:
        val = self._redis.get(key)
        return pickle.loads(val) if val else None


class GameLogic:
    def __init__(self, state_manager: StateManager, scenes_file_path: str) -> None:
        self._state_manager = state_manager
        self._commands = self._get_commands()
        self._operator_callbacks = self._get_operator_callbacks()
        self._scenes, self._start_scene = StoryLoader().load_story(scenes_file_path)
        SceneChecker().check_scenes(self._scenes, self._start_scene, list(self._commands.keys()))

    def start_game(self) -> str:
        self._state_manager.initialize()
        return self._visit_scene(self._start_scene)

    def _get_commands(self) -> Commands:
        return {
            'help': (
                'Show this help message',
                lambda contents: self._show_help_message()),
            'inventory': (
                'Show inventory',
                lambda contents: self._show_inventory()),
            'back': (
                'Go to previous scene',
                lambda contents: self._visit_previous_scene()),
            'restart': (
                'Restart game',
                lambda contents: self.start_game()),
        }

    def _get_operator_callbacks(self) -> ConditionalOperatorCallbacks:
        callbacks = {
            CONDITION_OPERATOR_HAS: self._has_item,
            CONDITION_OPERATOR_IS: self._is_switch_on,
        }
        callbacks = self._add_negation_operator_callbacks(callbacks)

        return callbacks

    def _add_negation_operator_callbacks(self, callbacks: ConditionalOperatorCallbacks) -> ConditionalOperatorCallbacks:
        # For each operator add also its negation operator (e.g. 'has' -> 'hasnot')
        return dict(callbacks, **dict([(operator + 'not', self._negate(callback)) for operator, callback in callbacks.items()]))

    def _negate(self, func: Callable) -> Callable:
        @wraps(func)
        def negate_func(*args, **kwargs):
            return not func(*args, **kwargs)
        return negate_func

    def _get_game_loop_actions(self) -> Actions:
        return [
            (lambda contents: self._is_popup_shown(),
                lambda contents: self._show_current_scene()),
            (lambda contents: self._user_entered_command(contents),
                lambda contents: self._execute_command(contents)),
            (lambda contents: self._user_entered_description_key(contents),
                lambda contents: self._show_description(contents)),
            (lambda contents: self._user_entered_item_key(contents),
                lambda contents: self._get_scene_item(contents)),
            (lambda contents: self._user_entered_switch_key(contents),
                lambda contents: self._set_switch(contents)),
            (lambda contents: self._user_entered_inventory_key(contents),
                lambda contents: self._show_description_for_inventory_key(contents)),
            (lambda contents: self._user_entered_transition_key(contents),
                lambda contents: self._go_to_next_scene(contents)),
            # Note: leave this last! (default action)
            (lambda contents: True,
                lambda contents: self._show_current_scene()),
        ]

    def run_game_logic(self, file_contents: str) -> str:
        predicate_and_action = self._get_game_loop_actions()
        file_contents = file_contents.strip()

        assert any([predicate(file_contents) for predicate, _ in predicate_and_action])
        for predicate, action in predicate_and_action:
            if predicate(file_contents):
                file_contents = action(file_contents)
                break

        return file_contents

    def _user_entered_command(self, file_contents: str) -> bool:
        callback = self._get_callback_for_command(file_contents)
        return callback is not None

    def _execute_command(self, file_contents: str) -> str:
        callback = self._get_callback_for_command(file_contents)
        return callback(file_contents)

    def _get_callback_for_command(self, file_contents: str) -> Callable:
        info_callback = self._get_dict_value_for_file_contents(self._commands,
                                                               file_contents)
        return info_callback[1] if info_callback else None

    def _user_entered_description_key(self, file_contents: str) -> bool:
        return self._get_description_for_key(file_contents) is not None

    def _show_description(self, file_contents: str) -> str:
        return self._show_popup(self._get_description_for_key(file_contents))

    def _get_description_for_key(self, file_contents: str) -> str:
        return self._get_dict_value_for_file_contents(self._get_current_scene()['descriptions'],
                                                      file_contents)

    def _user_entered_inventory_key(self, file_contents: str) -> bool:
        return self._get_description_for_inventory_key(file_contents) is not None

    def _show_description_for_inventory_key(self, file_contents: str) -> str:
        return self._show_popup(self._get_description_for_inventory_key(file_contents))

    def _get_description_for_inventory_key(self, file_contents: str) -> str:
        return self._get_dict_value_for_file_contents(self._state_manager.get_inventory(), file_contents)

    def _user_entered_item_key(self, file_contents: str) -> bool:
        return self._get_scene_item_for_key(file_contents) is not None

    def _get_scene_item(self, file_contents: str) -> str:
        item_name, item_description = self._get_scene_item_for_key(file_contents)
        if not self._state_manager.is_in_inventory(item_name):
            self._state_manager.add_to_inventory(item_name, item_description)
            return self._show_popup(f'You got: {item_name}!')
        else:
            return self._show_current_scene()

    def _get_scene_item_for_key(self, file_contents: str) -> Tuple[Key, str]:
        return self._get_dict_value_for_file_contents(self._get_current_scene()['items'],
                                                      file_contents)

    def _user_entered_switch_key(self, file_contents: str) -> bool:
        return self._get_switch_for_key(file_contents) is not None

    def _set_switch(self, file_contents: str) -> str:
        switch = self._get_switch_for_key(file_contents)
        if len(switch) == 3:
            name, enable_msg, disable_msg = list(switch)
            self._state_manager.toggle_switch(name)
            message = enable_msg if self._state_manager.is_switch_on(name) else disable_msg
            return self._show_popup(message)
        else:
            name, message = list(switch)
            if not self._state_manager.is_switch_on(name):
                self._state_manager.set_switch(name, True)
                return self._show_popup(message)
            else:
                return self._show_current_scene()

    def _get_switch_for_key(self, file_contents: str) -> Switch:
        return self._get_dict_value_for_file_contents(self._get_current_scene()['switches'],
                                                      file_contents)

    def _user_entered_transition_key(self, file_contents: str) -> bool:
        return self._get_next_scene(file_contents) is not None

    def _go_to_next_scene(self, file_contents: str) -> str:
        next_scene = self._get_next_scene(file_contents)
        return self._visit_scene(next_scene)

    def _get_next_scene(self, file_contents: str) -> SceneName:
        transition = self._get_dict_value_for_file_contents(self._get_current_scene()['transitions'],
                                                            file_contents)
        if transition and is_transition_conditional(transition):
            condition, true_scene, false_scene = split_transition_to_condition_and_scenes(transition)
            transition = true_scene if self._is_condition_true(condition) else false_scene

        return transition

    def _has_item(self, item: Key) -> bool:
        return self._state_manager.is_in_inventory(item)

    def _is_switch_on(self, switch: Key) -> bool:
        return self._state_manager.is_switch_on(switch)

    def _is_condition_true(self, condition: TransitionCondition) -> bool:
        operand_start = re.escape(CONDITION_OPERAND_START)
        operand_end = re.escape(CONDITION_OPERAND_END)

        any_operator = '|'.join(self._operator_callbacks.keys())
        regex = f'({any_operator}){operand_start}({KEY_REGEX}){operand_end}'

        condition = TransitionCondition(condition.strip())
        assert re.match('^(%s\\s*)+$' % regex, condition), 'regex: %s\ncondition: %s' % (regex, condition)

        return all([self._operator_callbacks[op](key) for op, key in re.findall(regex, condition)])

    def _visit_scene(self, scene_name: SceneName) -> str:
        if len(self._state_manager.get_scenes_visited()) == 0 or scene_name != self._get_current_scene()['name']:
            self._state_manager.append_scene_visited(self._scenes[scene_name])

        return self._show_current_scene()

    def _visit_previous_scene(self) -> str:
        if len(self._state_manager.get_scenes_visited()) > 1:
            self._state_manager.get_scenes_visited().pop()

        return self._show_current_scene()

    def _get_current_scene(self) -> dict:
        return self._state_manager.get_current_scene()

    def _show_current_scene(self) -> str:
        scene_text = self._get_current_scene()['text']
        self._state_manager.set_popup_shown(False)

        return scene_text

    def _show_popup(self, text: str, title: str = 'Info') -> str:
        content = f'=== {title} ===\n\n{text}\n\n(Save file to close this message)'
        self._state_manager.set_popup_shown(True)

        return content

    def _show_help_message(self) -> str:
        text = """- How to play
    - Edit file contents and then Save

- Special commands (append in the end of the file and Save):
""" + '\n'.join([f'    - {cmd}: {info}' for cmd, (info, callback) in self._commands.items()])
        return self._show_popup(text, 'Help')

    def _show_inventory(self) -> str:
        text = '\n'.join([f'- {item}' for item in self._state_manager.get_inventory()])
        return self._show_popup(text, 'Inventory')

    def _is_popup_shown(self) -> bool:
        return self._state_manager.is_popup_shown()

    def _get_dict_value_for_file_contents(self, d: Scene,
                                          file_contents: str,
                                          default=None) -> Any:
        result = default
        # Iterate in reverse order: if there's a default transition '', check it last
        for key, value in reversed(sorted(list(d.items()))):
            if file_contents.endswith(key):
                result = value
                break

        return result


class Game(EnforceOverrides):
    def __init__(self, game_logic: GameLogic) -> None:
        self.__game_logic = game_logic

    @final
    def run(self) -> None:
        self._pre_run()
        self.__visit_first_scene()
        self._main_loop()
        self._post_run()

    @final
    def __visit_first_scene(self) -> None:
        file_contents = self.__game_logic.start_game()
        self._set_content(file_contents)

    @final
    def _notify_file_was_modified(self) -> None:
        file_contents = self._get_content()
        file_contents = self.__game_logic.run_game_logic(file_contents)
        self._set_content(file_contents)

    def _pre_run(self) -> None:
        pass

    def _post_run(self) -> None:
        pass

    def _get_content(self) -> str:
        raise NotImplementedError

    def _set_content(self, content: str) -> None:
        raise NotImplementedError

    def _main_loop(self) -> None:
        # Must call _notify_file_was_modified() whenever file is modified
        raise NotImplementedError


class LocalFileGame(Game):
    def __init__(self, game_logic: GameLogic, file_path: str) -> None:
        super().__init__(game_logic)
        self._game_logic = game_logic
        self._file_path = os.path.realpath(file_path)
        self._file_dir = os.path.dirname(self._file_path)
        self._last_modification_time = 0.0

        # When user saves file, the game is alerted and the game logic runs,
        # which ultimately updates the file contents.
        # Thus, whenever user modifies the file, almost immediately the game
        # engine modifies the file again in response to user modification.
        # We use this threshold to avoid having this second file modification
        # trigger the game logic again.
        self._MIN_SECS_BETWEEN_SAVES = 0.5

    @overrides
    def _get_content(self) -> str:
        return open(self._file_path).read()

    @overrides
    def _set_content(self, content: str) -> None:
        with tempfile.NamedTemporaryFile(dir=self._file_dir, mode='w', delete=False) as tmpf:
            print(content, file=tmpf)
            os.rename(tmpf.name, self._file_path)

    def _on_file_modified(self, event: FileSystemEvent) -> None:
        if event.src_path == self._file_path:
            modification_time = os.stat(self._file_path).st_mtime
            sec_since_last_modification = modification_time - self._last_modification_time
            recenty_modified = sec_since_last_modification < self._MIN_SECS_BETWEEN_SAVES
            if not recenty_modified:
                self._last_modification_time = modification_time
                self._notify_file_was_modified()
            logging.info(f'{sec_since_last_modification:.3f} secs since last modification: update = {not recenty_modified}')

    @overrides
    def _main_loop(self) -> None:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self._on_file_modified

        observer = Observer()
        observer.schedule(event_handler, path=self._file_dir, recursive=False)
        observer.start()

        logging.info('Open file with your editor: %s' % self._file_path)

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class TestGame(Game):
    def __init__(self, game_logic: GameLogic, user_input_file_path: str, debug=False) -> None:
        super().__init__(game_logic)
        self._game_logic = game_logic
        self._user_input_file_path = user_input_file_path
        self._debug = debug
        self._expected_scene = None
        self._expected_condition = None

    @overrides
    def _pre_run(self) -> None:
        if not self._debug:
            logger = logging.getLogger()
            logger.disabled = True

    @overrides
    def _post_run(self) -> None:
        if not self._debug:
            logger = logging.getLogger()
            logger.disabled = True

    @overrides
    def _get_content(self) -> str:
        logging.warning(f'{self._file_contents}')
        return self._file_contents

    @overrides
    def _set_content(self, content: str) -> None:
        current_scene = self._game_logic._get_current_scene()['name']
        logging.info(f'=> {current_scene}\n{content}')
        if self._expected_scene:  # False only for the start scene
            assert self._expected_scene == current_scene, f'Expected scene: [{self._expected_scene}], current scene: [{current_scene}]'
        if self._expected_condition:
            assert self._game_logic._is_condition_true(self._expected_condition), f'Expected condition "{self._expected_condition}" is not true.'

    @overrides
    def _main_loop(self) -> None:
        for user_input in iter(ast.literal_eval(open(self._user_input_file_path).read())):
            if len(user_input) == 3:
                file_contents, expected_scene, expected_condition = user_input
            else:
                file_contents, expected_scene = user_input
                expected_condition = None
            if self._game_logic._is_popup_shown():
                self._file_contents = '(dummy save for popup scene)'
                self._expected_scene = self._game_logic._get_current_scene()['name']
                self._expected_condition = None
                self._notify_file_was_modified()

            self._file_contents = file_contents
            self._expected_scene = expected_scene
            self._expected_condition = expected_condition
            self._notify_file_was_modified()
