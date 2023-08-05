# Docker Dev Environment
Ddenv is a CLI tool to help with using docker as development environment.
It currently supports the following project management tools:
- yarn

## Installation
Ddenv requires Python 3.10+
```commandline
pip install ddenv
```

## Usage
```
$ ddenv --help
Usage: ddenv [OPTIONS] [COMMAND]...

  Run the command in a Docker container with all the dependencies and
  source code

Arguments:
  [COMMAND]...  The command to run

Options:
  -m, --manager TEXT              The project manager your project uses
                                  [required]
  -v, --version TEXT              The version of the project
                                  manager/runtime
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified
                                  shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell,
                                  to copy it or customize the installation.
  --help                          Show this message and exit.

```
Example:
```commandline
ddenv -m yarn yarn dev
```
