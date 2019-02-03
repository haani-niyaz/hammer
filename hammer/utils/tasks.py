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


def json_to_dict(data):
  """Covert json data to python dict

  Args:
    data (json): json paylod

  Returns:
    dict: json payload as a python dictionary

  Raises:
    TaskError: for any errors when attempting to convert json data to python dictionary

  """
  try:
    return json.loads(data)
  # Malformed json
  except TypeError as e:
    raise TasksError("Failed to load json data: {}".format(e))
