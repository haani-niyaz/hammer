import sys
import json
from ..utils.tasks import TasksError, run_cmd, json_to_dict


class KubeError(Exception):
  """An exception that occurs when action is performed on a role"""


class Kubectl(object):

  @staticmethod
  def _get_pod_data(cmd):
    try:
      return json_to_dict(run_cmd(cmd))
    except TasksError, e:
      raise KubeError(e)
