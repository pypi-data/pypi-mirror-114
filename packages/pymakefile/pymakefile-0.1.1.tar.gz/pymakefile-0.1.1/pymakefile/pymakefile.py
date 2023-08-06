import os
import click


@click.group()
def main():
    """
    Simple CLI for managing Makefile
    """
    pass


@main.command()
def init():
    makefile_exists = os.path.isfile("./Makefile")
    if not makefile_exists:
        with open("./Makefile", "a+") as f:
            f.write("# Makefile generated with pymakefile \n")
            f.write(
                "help:\n\t{0}\n".format(
                    """@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\\n", $$1, $$2}'\n"""
                )
            )
    else:
        print("Error: Makefile already exists")


@main.command()
@click.argument("name")
@click.argument("command")
@click.argument("description")
def add(name, command, description):
    makefile_exists = os.path.isfile("./Makefile")
    if not makefile_exists:
        print("Error: Makefile not found, you can create a new one using: pymake init")
    elif f"{name}:  ## " in open("./Makefile").read():
        print(f"Error: Makefile already has a command with name '{name}'")
    else:
        with open("./Makefile", "a+") as f:
            f.write(f"{name}:  ## {description}\n\t{command}\n\n")


if __name__ == "__main__":
    main()
