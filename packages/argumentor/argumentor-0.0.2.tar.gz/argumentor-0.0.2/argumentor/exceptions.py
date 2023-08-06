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


class ExecNameError(IOError):
    def __init__(self, *args):
        super(ExecNameError, self).__init__(*args)


class OperationExistsError(IOError):
    def __init__(self, *args):
        super(OperationExistsError, self).__init__(*args)


class OptionExistsError(IOError):
    def __init__(self, *args):
        super(OptionExistsError, self).__init__(*args)


class InvalidOptionError(IOError):
    def __init__(self, *args):
        super(InvalidOptionError, self).__init__(*args)


class ArgumentValueError(IOError):
    def __init__(self, *args):
        super(ArgumentValueError, self).__init__(*args)


class GroupExistsError(IOError):
    def __init__(self, *args):
        super(GroupExistsError, self).__init__(*args)


class GroupNotExistsError(IOError):
    def __init__(self, *args):
        super(GroupNotExistsError, self).__init__(*args)
