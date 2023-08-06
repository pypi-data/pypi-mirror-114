# argumentor - A library to work with command-line arguments
# Copyright (C) 2021 Twann <twann@ctemplar.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import re
from .exceptions import ExecNameError, OperationExistsError, OptionExistsError, ArgumentValueError, GroupExistsError, \
    GroupNotExistsError, InvalidOptionError

__version__ = '0.0.2'


class Arguments:

    def __init__(self, arguments: list = None, exec_name: str = None, generate_help_page: bool = True,
                 one_operation_required: bool = True, allow_short_args_together: bool = True) -> None:
        """
        Argumentor parser object
        :param arguments: Optional. Arguments to parse. If not set, sys.argv[1:] will be used
        :param exec_name: Optional. The name of the executable running. If not set, sys.argv[0] will be used
        :param generate_help_page: Defaults to True. Generate a help page as self.help_page
        :param one_operation_required: Defaults to True. If no operation is specified, the script will return an error
        :param allow_short_args_together: Defaults to True. Allow short arguments to be combined together
        (ex. '-vz' instead of '-v -z')
        """

        if arguments is None:
            self.arguments = sys.argv[1:]
        else:
            self.arguments = arguments

        if len(sys.argv) >= 1 and exec_name is None:
            self.exec_name = sys.argv[0]
        elif exec_name is None:
            raise ExecNameError('cannot find executable name')
        else:
            self.exec_name = exec_name

        self.generate_help_page = generate_help_page                    # Generate a help page
        self.one_operation_required = one_operation_required            # One operation is required
        self.allow_short_args_together = allow_short_args_together      # Allow short args to be combined

        self.operations = {}                                            # Available operations
        self.short_operations = {}                                      # Available short operations
        self.operation_groups = []                                      # Existing operation groups
        self.options = {}                                               # Available options
        self.short_options = {}                                         # Available short options
        self.option_groups = {}                                         # Existing option groups

        self.active_operation = None                                    # The operation that is running
        self.isolate_unmatched = True                                   # Invalid args are stored as operation value

        self.output_operations = {}                                     # Operations result after parsing
        self.output_options = {}                                        # Options result after parsing

    def add_operation(self, operation: str, value_type, description: str = None,
                      short_operation: str = None, required: bool = False, group: str = None) -> None:
        """
        Add an operation to the list of supported arguments
        :param operation: The operation (ex. '--help')
        :param value_type: The type of the value to catch (bool, str, int, list).
        :param description: Optional. The description of what the operation does
        :param short_operation: Optional. The short version of the operation (ex. '-h')
        :param required: Defaults to False. Choose if the operation is required or not
        :param group: Optional. Specify an operation group
        :return:
        """

        if operation in self.operations.keys():
            raise OperationExistsError(f'operation "{operation}" already exists')
        elif operation in self.options.keys():
            raise OptionExistsError(f'option "{operation}" already exists')
        elif short_operation is not None and short_operation in self.short_operations.keys():
            raise OperationExistsError(f'short operation "{operation}" already exists')
        elif short_operation is not None and short_operation in self.short_options.keys():
            raise OptionExistsError(f'short option "{operation}" already exists')
        elif value_type not in [bool, str, int, list]:
            raise ArgumentValueError(f'value type "{value_type}" is not supported')
        elif group is not None and group not in self.operation_groups:
            raise GroupNotExistsError(f'operation group "{group}" does not exist')
        elif short_operation is not None and len(short_operation) > 1 and not re.match(r'-[A-z0-9]', short_operation):
            raise InvalidOptionError(f'short operation can only be one-character long when no dash, not "{operation}"')
        elif short_operation is not None and len(short_operation) > 2:
            raise InvalidOptionError(f'short operation can contain a dash and a character maximum, not "{operation}"')
        else:
            self.operations[operation] = {
                'value_type': value_type,
                'description': description,
                'required': required,
                'group': group
            }
            if short_operation is not None:
                self.short_operations[short_operation] = operation

    def add_operation_group(self, group_name: str) -> None:
        """
        Create an operation group
        :param group_name: The name of the group
        :return:
        """

        if group_name in self.operation_groups:
            raise GroupExistsError(f'operation group "{group_name}" already exists')
        else:
            self.operation_groups.append(group_name)

    def add_options(self, option: str, value_type, description: str = None,
                    short_option: str = None, required: bool = False, available_with_operations: list = None,
                    required_by_operations: list = None, available_with_groups: list = None,
                    required_by_groups: list = None, group: str = None, inherit_from_group: bool = True) -> None:
        """
        Add an option to the list of supported arguments
        :param option: The option (ex. '--force')
        :param value_type: The type of the value to catch (bool, str, int, list).
        :param description: Optional. The description of what the operation does
        :param short_option: Optional. The short version of the operation (ex. '-f')
        :param required: Defaults to False. Choose if the operation is required or not
        :param available_with_operations: Optional. Option will only be available with operation in the list
        :param required_by_operations: Optional. Every operation in the list will fail without this option
        :param available_with_groups: Optional. Option will only be available with operation in the specified groups
        :param required_by_groups: Optional. Every operation in the specified groups will fail without this option
        :param group: Optional. Specify an option group
        :param inherit_from_group: Defaults to True. Inherit requirements and availability from group.
        :return:
        """
        if option in self.options.keys():
            raise OptionExistsError(f'option "{option}" already exists')
        elif option in self.operations.keys():
            raise OperationExistsError(f'operation "{option}" already exists')
        elif short_option is not None and short_option in self.short_options.keys():
            raise OptionExistsError(f'short option "{option}" already exists')
        elif short_option is not None and short_option in self.short_operations.keys():
            raise OperationExistsError(f'short operation "{option}" already exists')
        elif value_type not in [bool, str, int, list]:
            raise ArgumentValueError(f'value type "{value_type}" is not supported')
        elif group is not None and group not in self.option_groups.keys():
            raise GroupNotExistsError(f'option group "{group}" does not exist')
        elif not re.match(r'--[A-z0-9\-]*', option):
            raise InvalidOptionError(f'option should start with two dashes: "--", not "{option}"')
        elif short_option is not None and len(short_option) != 2:
            raise InvalidOptionError(f'short option must be two-characters long, not "{option}"')
        elif short_option is not None and not re.match(r'-[A-z0-9]', short_option):
            raise InvalidOptionError(f'short option must start with a dash and finish with a character, not "{option}"')
        else:
            if group is not None and inherit_from_group:
                self.options[option] = {
                    'value_type': value_type,
                    'description': description,
                    'required': required,
                    'group': group,
                    'available_with_operations': self.option_groups[group]['available_with_operations'],
                    'required_by_operations': self.option_groups[group]['required_by_operations'],
                    'available_with_groups': self.option_groups[group]['available_with_groups'],
                    'required_by_groups': self.option_groups[group]['required_by_groups']
                }
                if available_with_operations is not None:
                    self.options[option]['available_with_operations'] = available_with_operations
                if required_by_operations is not None:
                    self.options[option]['required_by_operations'] = required_by_operations
                if available_with_groups is not None:
                    self.options[option]['available_with_groups'] = available_with_groups
                if required_by_groups is not None:
                    self.options[option]['required_by_groups'] = required_by_groups
            else:
                self.options[option] = {
                    'value_type': value_type,
                    'description': description,
                    'required': required,
                    'group': group,
                    'available_with_operations': available_with_operations,
                    'required_by_operations': required_by_operations,
                    'available_with_groups': available_with_groups,
                    'required_by_groups': required_by_groups
                }

            if short_option is not None:
                self.short_options[short_option] = option

    def add_option_group(self, group_name: str, available_with_operations: list = None,
                         required_by_operations: list = None, available_with_groups: list = None,
                         required_by_groups: list = None) -> None:
        """
        Create an option group
        :param group_name: The name of the groups
        :param available_with_operations: Optional. Options will only be available with operation in the list
        :param required_by_operations: Optional. Every operation in the list will fail without these options
        :param available_with_groups: Optional. Options will only be available with operation in the specified groups
        :param required_by_groups: Optional. Every operation in the specified groups will fail without these options
        :return:
        """

        if group_name in self.option_groups.keys():
            raise GroupExistsError(f'option group "{group_name}" already exists')
        else:
            self.option_groups[group_name] = {
                'available_with_operations': available_with_operations,
                'required_by_operations': required_by_operations,
                'available_with_groups': available_with_groups,
                'required_by_groups': required_by_groups
            }

    def __match_operation(self, operation_title: str, real_operation: str, real_argument: str) -> None:

        if self.active_operation is None:

            self.active_operation = operation_title

            if self.operations[operation_title]['value_type'] == bool:
                self.output_operations[operation_title] = True
            elif len(self.arguments) - self.arguments.index(real_argument) > 1:
                if self.operations[operation_title]['value_type'] == int:
                    try:
                        self.output_operations[operation_title] = int(self.arguments[self.arguments.index(real_argument) + 1])
                    except ValueError:
                        print(f'Error: operation "{real_operation}" requires an integer')
                        sys.exit(1)
                    else:
                        self.arguments.pop(self.arguments.index(real_argument) + 1)
                elif self.operations[operation_title]['value_type'] == str:
                    self.output_operations[operation_title] = str(self.arguments[self.arguments.index(real_argument) + 1])
                    self.arguments.pop(self.arguments.index(real_argument) + 1)
                elif self.operations[operation_title]['value_type'] == list:
                    self.output_operations[operation_title] = []
                    self.isolate_unmatched = True
                else:
                    raise ArgumentValueError(f'invalid value type: "{self.operations[operation_title]["value_type"]}"')
            else:
                print(f'Error: operation "{real_operation}" requires at least one argument')
                sys.exit(1)
        else:

            print('Error: only one operation at the same time is supported')
            sys.exit(1)

    def __match_option(self, option_title: str, real_option: str, real_argument: str) -> None:

        if self.active_operation is not None and self.options[option_title]['available_with_operations'] is not None and not self.active_operation in self.options[option_title]['available_with_operations']:
            print(f'Error: option "{real_option}" is not available with operation "{self.active_operation}"')
            sys.exit(1)

        elif self.active_operation is not None and self.options[option_title]['available_with_groups'] is not None and self.operations[self.active_operation]['group'] not in self.options[option_title]['available_with_groups']:
            print(f'Error: option "{real_option}" is not available with operation "{self.active_operation}"')
            sys.exit(1)

        elif self.active_operation is not None or not self.one_operation_required:

            if self.options[option_title]['value_type'] == bool:
                self.output_options[option_title] = True
            elif len(self.arguments) - self.arguments.index(real_argument) > 1:
                if self.options[option_title]['value_type'] == int:
                    try:
                        self.output_options[option_title] = int(self.arguments[self.arguments.index(real_argument) + 1])
                    except ValueError:
                        print(f'Error: operation "{real_option}" requires an integer')
                        sys.exit(1)
                    else:
                        self.arguments.pop(self.arguments.index(real_argument) + 1)
                elif self.options[option_title]['value_type'] == str:
                    self.output_options[option_title] = str(self.arguments[self.arguments.index(real_argument) + 1])
                    self.arguments.pop(self.arguments.index(real_argument) + 1)
                elif self.options[option_title]['value_type'] == list:
                    self.output_options[option_title] = []
                    for value in self.arguments[self.arguments.index(real_argument) + 1:]:
                        if re.match(r'-[A-z0-9_.\-]*', value):
                            break
                        else:
                            self.output_options[option_title].append(value)
                            self.arguments.remove(value)
                else:
                    raise ArgumentValueError(f'invalid value type: "{self.options[option_title]["value_type"]}"')
            else:
                print(f'Error: option "{real_option}" requires at least one argument')
                sys.exit(1)

    def parse(self) -> [dict, dict]:
        """
        Parse all arguments and return matches
        :return: operations, options
        """

        for argument in self.arguments:

            if argument in self.operations.keys():

                self.__match_operation(
                    operation_title=argument,
                    real_operation=argument,
                    real_argument=argument
                )

            elif argument in self.options.keys():

                self.__match_option(
                    option_title=argument,
                    real_option=argument,
                    real_argument=argument
                )

            elif argument in self.short_operations.keys():

                self.__match_operation(
                    operation_title=self.short_operations[argument],
                    real_operation=argument,
                    real_argument=argument
                )

            elif argument in self.short_options.keys():

                self.__match_option(
                    option_title=self.short_options[argument],
                    real_option=argument,
                    real_argument=argument
                )

            elif self.allow_short_args_together and len(argument) > 1 and (argument[0:1] in self.short_operations.keys()) or (argument[0:2] in self.short_operations.keys()):

                for character in argument.replace('-', ''):

                    if character in self.short_operations.keys() or f'-{character}' in self.short_operations.keys():
                        short_argument = character if character in self.short_operations.keys() else f'-{character}'

                        self.__match_operation(
                            operation_title=self.short_operations[short_argument],
                            real_operation=short_argument,
                            real_argument=argument
                        )

                    elif character in self.short_options.keys() or f'-{character}' in self.short_options.keys():
                        short_argument = character if character in self.short_options.keys() else f'-{character}'

                        self.__match_option(
                            option_title=self.short_options[short_argument],
                            real_option=short_argument,
                            real_argument=argument
                        )

                    else:
                        print(f'Error: invalid argument "{character}" in "{argument}"')
                        sys.exit(1)

            elif self.allow_short_args_together and len(argument) > 1 and argument[0:2] in self.short_options.keys():

                for character in argument.replace('-', ''):

                    if character in self.short_options.keys() or f'-{character}' in self.short_options.keys():
                        short_argument = character if character in self.short_options.keys() else f'-{character}'

                        self.__match_option(
                            option_title=self.short_options[short_argument],
                            real_option=short_argument,
                            real_argument=argument
                        )

                    elif character in self.short_operations.keys() or f'-{character}' in self.short_operations.keys():
                        print('Error: operation must be specified before any other arguments')
                        sys.exit(1)

                    else:
                        print(f'Error: invalid argument "{character}" in "{argument}"')
                        sys.exit(1)

            elif self.isolate_unmatched and self.active_operation is not None and not re.match(r'-[A-z0-9_.\-]*', argument):

                self.output_operations[self.active_operation].append(argument)

            else:

                print(f'Error: invalid argument "{argument}"')
                sys.exit(1)

        for active_operation in self.output_operations.keys():
            if self.operations[active_operation]['value_type'] == list and  self.output_operations[active_operation] == []:
                print(f'Error: option "{active_operation}" requires at least one argument')
                sys.exit(1)
        for operation in self.operations:
            if self.operations[operation]['required'] and operation not in self.output_operations.keys():
                print(f'Error: operation "{operation}" is required')
                sys.exit(1)
        for option in self.options:
            if self.options[option]['required'] and option not in self.output_options.keys():
                print(f'Error: option "{option}" is required')
                sys.exit(1)
            if self.options[option]['required_by_operations'] is not None and option not in self.output_options:
                for required in self.options[option]['required_by_operations']:
                    if required in self.output_operations.keys():
                        print(f'Error: operation "{required}" requires the option "{option}"')
                        sys.exit(1)

        return self.output_operations, self.output_options
