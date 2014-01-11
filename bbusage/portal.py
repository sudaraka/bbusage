#  portal.py: sub-routines for VAS portal HTTP queries
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


import requests

from .config import *


class Portal:
    """ Sub-routines for accessing VAS Portal data via HTTP requests. """


    # cookie container for the current session
    _session_cookies = None


    def authnticate(self, username, password):
        """ (str, str) -> bool

        Create new session on the VAS Portal, login and store the generated cookies
        to maintain session for future requests.

        """

        login_param = {'j_username': username, 'j_password': password}

        try:
            # Initialize a new session by opening the portal URL
            response = requests.get(PORTAL_URL)

            # Send login parameters via HTTP POST along with the session cookie
            # received from earlier request.
            response = requests.post(PORTAL_URL + PORTAL_URI_LOGIN, data=login_param,
                                    cookies=response.cookies)

            if('pragma' not in response.headers or
            'cache-control' not in response.headers or
            'set-cookie' not in response.headers or
            'Invalid Credentials' in response.text):
                return False

            self._session_cookies = response.cookies
        except:
            return False

        return True

    def get_profile(self):
        """ (None) -> dict

        Returns a dict with profile data for user currently authenticated or
        None in case of an invalid session or HTTP request failure.

        """

        if(None == self._session_cookies):
            return None

        try:
            response = requests.get(PORTAL_URL + PORTAL_URI_PROFILE,
                                    cookies=self._session_cookies)

            self._session_cookies = response.cookies

            return response.json()
        except:
            pass

        return None
