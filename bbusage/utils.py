#  utils.py: shared calculations and formatting for bbusage
#  Copyright 2014 Sudaraka Wijesinghe <sudaraka.org/contact>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


def metric_bytes(byte_value):
    """ (int) -> dict

    Return the given byte value as metric unit and value in a dict.

    """

    units = ['b', 'K', 'M', 'G', 'T']

    while 1024 < byte_value:
        byte_value /= 1024.0
        units.pop(0)

        if 1 >= len(units):
            break

    return {'value': byte_value, 'unit': units[0]}
