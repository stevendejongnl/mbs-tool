import os
import subprocess
import textwrap
from glob import glob

import inquirer
from ruamel.yaml import SafeConstructor, YAML
from slugify import slugify


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def console_print(text, console_type=None):
    if console_type == 'header':
        print(f"{Colors.HEADER}{text}{Colors.END}")

    elif console_type == 'header_underline':
        print(f"{Colors.HEADER}{Colors.UNDERLINE}{text}{Colors.END}{Colors.END}")

    elif console_type == 'blue':
        print(f"{Colors.BLUE}{text}{Colors.END}")

    elif console_type == 'cyan':
        print(f"{Colors.CYAN}{text}{Colors.END}")

    elif console_type == 'green':
        print(f"{Colors.GREEN}{text}{Colors.END}")

    elif console_type == 'warning':
        print(f"{Colors.WARNING}{text}{Colors.END}")

    elif console_type == 'fail':
        print(f"{Colors.FAIL}{text}{Colors.END}")

    elif console_type == 'bold':
        print(f"{Colors.BOLD}{text}{Colors.END}")

    elif console_type == 'underline':
        print(f"{Colors.UNDERLINE}{text}{Colors.END}")

    else:
        print(text)


def construct_yaml_map(self, node):
    # test if there are duplicate node keys
    data = []
    yield data
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=True)
        val = self.construct_object(value_node, deep=True)
        data.append((key, val))


def parse_scripts():
    SafeConstructor.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)
    yaml = YAML(typ='safe')

    scripts = {}
    for yaml_file in glob('./scripts/**/*.yml', recursive=True):
        with open(yaml_file) as file:
            file_path, file_name = os.path.split(yaml_file)
            yaml_list = yaml.load(file)

            scripts[slugify(file_name)] = yaml_list

    return scripts


def run_commands(commands):
    for command in commands:
        process = None
        if isinstance(command[1], str):
            multiline_command = command[1].replace('\\n', '\n').replace('\\t', '\t')

            process = subprocess.run(
                multiline_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)

        if isinstance(command[1], list):
            process = subprocess.Popen(
                command[1],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=0)

        for outLine in process.stdout:
            console_print(outLine.strip(), 'green')
        for outLine in process.stderr:
            console_print(outLine.strip(), 'fail')


def get_functions(functions):
    function_list = []

    for name, commands in functions:
        function_list.append(name)

    return function_list


def build_functions(functions):
    for name, commands in functions:
        console_print(name, 'header')
        run_commands(commands)


def build_shell():
    parsed_scripts = parse_scripts()

    for script in parsed_scripts:
        name, functions = parsed_scripts[script]
        console_print(name[1], 'header_underline')
        build_functions(functions[1])


def init():
    # Calls for an infinite loop that keeps executing
    # until an exception occurs
    while True:
        parsed_scripts = parse_scripts()

        script_list = []
        function_list = {}
        for script in parsed_scripts:
            name, functions = parsed_scripts[script]
            script_list.append(name[1])
            function_list[name[1]] = get_functions(functions[1])

        questions = [
            inquirer.List(
                'script',
                message="Let's do something!",
                choices=script_list,
            )
        ]

        try:
            script_choice = inquirer.prompt(questions)

            try:
                print(function_list[script_choice['script']])

            except ValueError:
                print('joe')

        # If something else that is not the string
        # version of a number is introduced, the
        # ValueError exception will be called.
        except ValueError:
            # The cycle will go on until validation
            print("Error! This is not a number. Try again.")

        # When successfully converted to an integer,
        # the loop will end.
        else:
            # print("Impressive, ", test4word, "! You spent", test4num * 60, "minutes or", test4num * 60 * 60,
            #       "seconds in your mobile!")
            break
    # build_shell()


if __name__ == '__main__':
    init()
