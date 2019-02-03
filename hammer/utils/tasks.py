"""Tasks"""

import os
import errno
import pwd
from subprocess import Popen, PIPE, check_output, CalledProcessError
import sys
import json


class TasksError(Exception):
  """An exception that occurs when performing administrative operations"""
  pass
