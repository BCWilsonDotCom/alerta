#
# NOTE: This file is overwritten by TeamCity for a production release.
#

import os
import datetime

BUILD_NUMBER = 'DEV'
BUILD_DATE = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
BUILD_VCS_NUMBER = 'unknown'
BUILT_BY = os.environ.get('USER', 'unknown')
HOSTNAME = os.uname()[1]
