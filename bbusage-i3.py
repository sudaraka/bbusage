#!/usr/bin/env python
#
#  bbusage-i3.py: Display remaining broadband data usage for i3-bar/conky.
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
#  USAGE: bbusage-i3.py <vas_portal_username> <password>
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


# Start main application
if '__main__' == __name__:
    if 3 > len(sys.argv):
        print('0.00G')
        sys.exit(1)

    # Get data
    p = Portal()
    if not p.authnticate(sys.argv[1], sys.argv[2]):
        print('0.00G')
        sys.exit(1)

    data = p.get_profile()
    if data is None:
        print('0.00G')
        sys.exit(1)

    # Print result
    remaining_bytes = min(int(data['totalrem']), int(data['peakrem']))
    tmp = metric_bytes(remaining_bytes)

    print('%s%s' % (('%.2f' % tmp['value']), tmp['unit']))
