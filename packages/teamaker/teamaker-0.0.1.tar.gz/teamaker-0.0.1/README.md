<div align="center">
  <img src="https://i.imgur.com/RqmnV9P.png" alt="TEA Maker" width="150">
</div>

# teamaker

Minimal game engine to create and play **t**ext-**e**dit **a**dventures.

[![Python package](https://github.com/gmargari/teamaker/actions/workflows/python-package.yml/badge.svg)](https://github.com/gmargari/teamaker/actions/workflows/python-package.yml)

## Install

```sh
pip install virtualenv
virtualenv venv --python=python3 
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```sh
source venv/bin/activate
python game.py examples/house_story.py
```
Then open `openme.txt` with your text editor.

<details><summary>Note on text editor</summary>
For improved experience, your text editor should support auto-reload of externally modified files, without any prompt.

We strongly suggest the (open-source) Notepad2 as modified by [sheepolution](https://github.com/Sheepolution) in [And yet it hurts](https://sheepolution.com/blog/gamedev/how-i-made-a-game-played-in-notepad/) exactly for this reason.
</details>

## Test

```sh
python game.py examples/house_story.py -t examples/house_story.test
```


## Notes

[Icon](https://thenounproject.com/term/tea/4137/) by [Jacob Halton](https://jacobhalton.carrd.co).
