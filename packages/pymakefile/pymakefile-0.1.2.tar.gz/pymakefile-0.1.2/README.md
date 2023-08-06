# pymakefile
Manage your Makefiles with python

## Install
```
pip install pymakefile
```
## Usage

### Starting a new Makefile
```console
pymake init
```

### Add a new command to the Makefile
```
pymake add '{command_name}' '{command}' '{description}'
```  

Example of adding new command:  
```
pymake add runlocal 'python manage.py runserver' 'Starts the development server'
```

### Show available commands in Makefile
```
make help
```

## Development
### Install dependencies
```
poetry install
```
### Activate virtualenv
```
poetry shell
```
### Running the commands from source
```
python pymakefile.py init
```
```
python pymakefile.py add '{command_name}' '{command}' '{description}'
```

### Applying lint rules
```
black .
```
