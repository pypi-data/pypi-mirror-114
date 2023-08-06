import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='teamaker',
    version='0.0.1',
    description='Minimal game engine to create and play text-edit adventures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gmargari/teamaker',
    project_urls={
        'Bug Tracker': 'https://github.com/gmargari/teamaker/issues',
    },
    # Packages the project depends on to run. pip will also install this when
    # the project is installed
    install_requires=[
        'Cerberus',
        'overrides',
        'watchdog',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Giorgos Margaritis',
    author_email='gmargari@protonmail.com',
    license='MIT',
    packages=[
        'teamaker'
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
