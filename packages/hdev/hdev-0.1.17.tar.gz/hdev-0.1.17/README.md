# hdev

The CLI for the Hypothesis development environment.

Installation & Upgrading
------------------------

The instructions below use [pipx](https://pipxproject.github.io/pipx/) to
install `hdev`. `pipx` will install `hdev` in its own isolated virtualenv at
`~/.local/pipx/venvs/hdev` and add it to your `PATH`, without `sudo`. You can
easily uninstall it again with `pipx uninstall hdev`. It won't touch your
system Python environment at all.

### Installing on macOS

Install [Homebrew](https://brew.sh/) and then run:

```shellsession
brew install pipx
pipx ensurepath
pipx install hdev
```

### Installing on Linux

```shellsession
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install hdev
```

### Upgrading (on either macOS or Linux)

To upgrade hdev to the latest version:

```shellsession
pipx upgrade hdev
```

Usage
-----

```
usage: hdev [-h] [--project PROJECT_DIR] [--find FIND_COMMAND] [--debug] {alembic,clean,config,deps,install-python,python_version,requirements,run,template} ...

positional arguments:
  {alembic,clean,config,deps,install-python,python_version,requirements,run,template}
    alembic             Run alembic commands to create and execute DB migrations.
    clean               Clean a project directory
    config              Get format and run data from pyproject.toml
    deps                Get dependency information
    install-python      Install the versions of python listed in the `.python-version` file.
    python_version      Dump the versions of Python in various formats
    requirements        Compiles .txt requirements file based on the existing .in files using pip-tools
    run                 Run a custom command defined in the pyproject.toml file
    template            Update the local project template

optional arguments:
  -h, --help            show this help message and exit
  --project PROJECT_DIR
                        Path of the project's root. Defaults to '.'. Can be specified multiple times
  --find FIND_COMMAND   Find projects from the current directory. This can be one of 'APPS', 'LIBS', 'ANY' or a comma separated list of project names.
  --debug               Enable debugging info

```

Configuration
-------------

`hdev` is configured within your project's `pyproject.toml` file with the following options:

```toml
[tool.hdev]
project_name = "myproject"
project_type = "library"   # Or "application"

[tool.hdev.clean]
# File and directory patterns relative to the root to remove.
# These support shell expansions and patterns
files=["dir/sub_dir/my_specific_file.txt"]
dirs=["resources/__myapp_cache__"]
# File and directory names which will be removed anywhere they
# are found. These support shell expansions and patterns
file_names=["*.ini"]
dir_names=["_cache_*"]
# Control if empty dirs are cleaned or not
empty_dirs=false

[tool.hdev.run]
# Add a custom command runnable with `hdev run custom`
mycommand.command = "echo hello"
mycommand.help = "Say hello!"
```

You can choose to not use any configuration, in that case `hdev` provides
sensible default for most Hypothesis projects.

Hacking
-------

### Installing hdev in a development environment

#### You will need

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  * Follow the instructions in the pyenv README to install it
  * On macOS: the Homebrew method works best on macOS
  * On Ubuntu: follow the Basic GitHub Checkout method

* [Graphviz](https://graphviz.org/) \[optional\]
  * This is only needed for the `hdev deps --graph` command
  * On macOS: `brew install graphviz`
  * On Ubuntu: `sudo apt install graphviz`

#### Clone the git repo

```terminal
git clone https://github.com/hypothesis/hdev.git
```

This will download the code into a `hdev` directory
in your current working directory. You need to be in the
`hdev` directory for the rest of the installation
process:

```terminal
cd hdev
```

#### Run the tests

```terminal
make test
```

**That's it!** You’ve finished setting up your hdev
development environment. Run `make help` to see all the commands that're
available for linting, code formatting, packaging, etc.

### Updating the Cookiecutter scaffolding

This project was created from the
https://github.com/hypothesis/h-cookiecutter-pypackage/ template.
If h-cookiecutter-pypackage itself has changed since this project was created, and
you want to update this project with the latest changes, you can "replay" the
cookiecutter over this project. Run:

```terminal
make template
```

**This will change the files in your working tree**, applying the latest
updates from the h-cookiecutter-pypackage template. Inspect and test the
changes, do any fixups that are needed, and then commit them to git and send a
pull request.

If you want `make template` to skip certain files, never changing them, add
these files to `"options.disable_replay"` in
[`.cookiecutter.json`](.cookiecutter.json) and commit that to git.

If you want `make template` to update a file that's listed in `disable_replay`
simply delete that file and then run `make template`, it'll recreate the file
for you.
