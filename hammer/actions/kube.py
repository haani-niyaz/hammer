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


class Pod(object):

  def __init__(self, name, namespace='default'):
    """Initialize pod object

    Raises:
        KubeError: notify user of errors encoutered when running kubectl commands
    """

    self.name = name
    self.namespace = namespace

    try:
      self._data = Kubectl._get_pod_data(
          "kubectl get po {0} -n {1} -o json".format(self.name, self.namespace))
      self.pvcs = self._get_persistent_volume_claims()
    except TasksError as e:
      raise KubeError(e)

  def _get_persistent_volume_claims(self):
    result = {}
    for v in self._data['spec']['volumes']:
      if 'persistentVolumeClaim' in v:
        result[v['name']] = v['persistentVolumeClaim']['claimName']
    return result
