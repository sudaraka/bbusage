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


from bbusage.portal import Portal

# Start main application
if '__main__' == __name__:
    p = Portal()
    p.authnticate('mhg2847002', '')
    print(p.get_profile())
