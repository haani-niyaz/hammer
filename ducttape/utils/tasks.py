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


def pprint(parsed):
  return json.dumps(parsed, indent=4, sort_keys=True)


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


def run_cmd(cmd):
  """Run command and print output

  Args:
      cmd (str): unix command string

  Raises:
      TasksError: validates if the 'command' to execute exists in the user's path
  """

  cmd = cmd.split()
  try:
    check_output(['which', cmd[0]])
  except CalledProcessError, e:
    raise TasksError("Is '{0}' executable in your path?".format(cmd[0]))

  process = Popen(cmd, stdout=PIPE, stderr=PIPE)
  # Wait for child process to terminate before checking exit code
  process.wait()

  # Return stdout if no failures
  if process.returncode == 0:
    return process.stdout.read()
  else:
    message = ''.join(process.stderr)
    raise TasksError(message)
