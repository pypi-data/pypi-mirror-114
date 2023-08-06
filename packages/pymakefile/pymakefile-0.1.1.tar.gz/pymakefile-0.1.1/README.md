# pymakefile
Manage your Makefiles from python

## Install

## Usage

### Starting a new Makefile
`pymake init`

### Add a new command to the Makefile
`pymake add '{command_name}' '{command}' '{description}'`  
Example:  
`pymake add runlocal 'python manage.py runserver' 'Starts the development server'`

## Development
### Install dependencies
`poetry install`
### Activate virtualenv
`poetry shell`
### Running the commands from source
- `python pymakefile.py init`
- `python pymakefile.py add '{command_name}' '{command}' '{description}'`

### Applying lint rules
`black .`
