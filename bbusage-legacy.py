#!/usr/bin/env python
#
#  bbusage-legacy.py: Grab and display SLT ADSL Usage data from online usage meter
#  Copyright 2012 Sudaraka Wijesinghe <sudaraka.org/contact>
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
#  USAGE: bbusage-legacy.py <broadband_username> [number_of_months]
#
#  DISCLAIMER:
#  General public is encourage NOT to use this code for financial gain or any
#  form of act that will result in harm to any person or company. Author will
#  NOT be responsible of such usage.
#
#  METHODOLOGY:
#  This program exploit the fact that SLT Broadband usage meter result page
#  (http://webusage.slt.lk:8080/servlet/BmsWeb as of 11/30/2012) does not
#  require a valid login session in order to generate the usage report.
#



import sys
import re
import datetime
import urllib
import httplib2



USAGE_METER_URL     = 'http://webusage.slt.lk:8080/servlet/BmsWeb'
USAGE_METER_SERVICE = 'SLTBB'



#  Print the usage information
# ============================================================================
def print_usage():
  print '''
USAGE: bbusage-legacy.py <broadband_username> [number_of_months]

  broadband_username    username assigned to you by the ISP
  number_of_months      Number of previous months to display (default = 1)
'''



#  Extract usage volume from CDR text
# ============================================================================
def get_bb_usage(user, year, month):
  month_flag = datetime.date(year, month, 1).strftime('%b/%Y').upper()

  # Get CDR text
  cdr_text = get_cdr(user, month_flag)

  try:
    # Check for 'No Records' text and return if it's there
    if 'No Records Found' in cdr_text:
      return None

    # Find the last row with caption "Total" as a keyword
    cdr_text = cdr_text.split('Total')[1]

    # Find the volume cdr_text nnn,nnn.nn MB
    match = re.search(r'([\d,\.]+)\s+MB', cdr_text)
    volume = match.group(1).replace(',', '')
  except:
    return None

  # Return volume in Giga bytes
  return float(volume) / 1024



#  Get CDR text over HTTP POST
# ============================================================================
def get_cdr(user, month_flag):
  http = httplib2.Http()

  try:
    # Get text via HTTP POST
    text = http.request(USAGE_METER_URL, 'POST',
      urllib.urlencode({
        'service':USAGE_METER_SERVICE,
        'userName':user,
        'mon1':month_flag,
        'mon2':'N',
        'mon3':'N',
        'I1':'submit'
      }),
      {
        'Content-Type':'application/x-www-form-urlencoded'
      }
    )
  except:
    return None

  return text[1]



#  Main program
# ============================================================================
if '__main__' == __name__:
  if 2 > len(sys.argv):
    print_usage()
    sys.exit(1)

  # Sanitize the user name
  bbuser = sys.argv[1]
  if '@' in bbuser:
    bbuser = bbuser.split('@')[0]

  if None == re.match('^[a-z]{2,3}\d{7,10}$', bbuser):
    print 'Invalid broadband username:', sys.argv[1]
    sys.exit(1)

  # Number of previous months to load data from
  # Use the second command line parameter only if it is an integer
  try:
    nof_months = int(sys.argv[2])
  except:
    nof_months = 1

  asked_months = nof_months

  # Display usage starting from current month and nof_months  backwards
  cdr_year = datetime.date.today().year
  cdr_month = datetime.date.today().month

  print '+' + ('-' * 30) + '+'
  print '| Year |', 'Month'.ljust(9), '|', 'Usage |'.rjust(11)
  print '+' + ('-' * 30) + '+'

  try:
    while 0 < nof_months:
      volume = get_bb_usage(bbuser, cdr_year, cdr_month)

      if None == volume:
        print \
          '|', \
           datetime.date(cdr_year, cdr_month, 1) \
            .strftime('No data for %b,%Y') \
            .center(28), \
          '|'

        if 1 == asked_months or nof_months != asked_months:
          break
      else:
        print \
          '|', \
          datetime.date(cdr_year, cdr_month, 1).strftime('%Y'), '|', \
          datetime.date(cdr_year, cdr_month, 1).strftime('%B').ljust(9), '|', \
          '{:.2f} GB'.format(volume).rjust(9), '|'

      # Prepare for the next round
      nof_months = nof_months - 1
      cdr_month = cdr_month -1

      if 1 > cdr_month:
        cdr_month = 12
        cdr_year = cdr_year - 1
  except KeyboardInterrupt:
    print ''
  finally:
    print '+' + ('-' * 30) + '+'
