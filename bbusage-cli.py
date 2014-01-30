#!/usr/bin/env python
#
#  bbusage-cli.py: Display remaining broadband data usage VAS portal.
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
#  USAGE: bbusage-cli.py <vas_portal_username> <password>
#
#  DISCLAIMER:
#  General public is encourage NOT to use this code for financial gain or any
#  form of act that will result in harm to any person or company. Author will
#  NOT be responsible of such actions of the user.
#


import calendar
import sys

from datetime import datetime

from bbusage.portal import Portal
from bbusage.utils import metric_bytes


COL_WIDTH = [27, 6]


def print_usage():
    """ (None) -> None
    Output the usage message when script is executed with incorrect number of
    parameters.

    """

    print('''USAGE: %s <vas_profile_username> <password>

  vas_portal_username   username you registered with ISP VAS Portal
  password              password for the VAS Portal user
''' % sys.argv[0])


# Start main application
if '__main__' == __name__:
    if 3 > len(sys.argv):
        print_usage()
        sys.exit(1)

    print('''bbusage Copyright 2014 Sudaraka Wijesinghe <sudaraka.org/contact>
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions under GNU GPLv3 or later.
''')

    # Get data
    p = Portal()
    if not p.authnticate(sys.argv[1], sys.argv[2]):
        print('Incorrect username or password')
        print('')

        sys.exit(1)

    data = p.get_profile()
    if data is None:
        print('Unable to fetch usage data')

        sys.exit(1)

    remaining_days = calendar.monthrange(datetime.now().year,
                                         datetime.now().month)[1]
    remaining_days -= datetime.now().day

    remaining_minutes_today = (23 - datetime.now().hour) * 60
    remaining_minutes_today += 59 - datetime.now().minute

    min_usage = min([int(data['totalrem']), int(data['peakrem'])])
    per_minute_usage = min_usage / (remaining_minutes_today + (remaining_days * 24 * 60))

    # Print result
    print('+' + ('-' * (sum(COL_WIDTH) + 6)) + '+')

    tmp = metric_bytes(int(data['totalrem']))
    print('| %s | %s%s |' % ('Total Remaining'.ljust(COL_WIDTH[0]),
                            ('%.2f' % tmp['value']).rjust(COL_WIDTH[1]),
                            tmp['unit']))

    tmp = metric_bytes(int(data['peakrem']))
    print('| %s | %s%s |' % ('Peak Remaining'.ljust(COL_WIDTH[0]),
                            ('%.2f' % tmp['value']).rjust(COL_WIDTH[1]),
                            tmp['unit']))

    print('+' + ('-' * (sum(COL_WIDTH) + 6)) + '+')

    print('| %s | %s  |' % ('Possible usage'.ljust(COL_WIDTH[0]),
                            ''.rjust(COL_WIDTH[1])))

    tmp = metric_bytes(per_minute_usage * remaining_minutes_today)
    print('| %s | %s%s |' % (' - Remainder of today'.ljust(COL_WIDTH[0]),
                            ('%.2f' % tmp['value']).rjust(COL_WIDTH[1]),
                            tmp['unit']))

    if 0 < remaining_days:
        tmp = metric_bytes(per_minute_usage * 24 * 60)
        print('| %s | %s%s |' % ((' - Following %2d days (each)' %
                remaining_days).ljust(COL_WIDTH[0]), ('%.2f' %
                tmp['value']).rjust(COL_WIDTH[1]), tmp['unit']))

    print('+' + ('-' * (sum(COL_WIDTH) + 6)) + '+')
    print('')
