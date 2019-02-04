import sys
import json
from ..utils.tasks import TasksError, run_cmd, json_to_dict, pprint


class KubeError(Exception):
  """An exception that occurs when action is performed on a role"""


class Kubectl(object):

  def __init__(self, name, namespace):
    self.name = name
    self.namespace = namespace

  @staticmethod
  def _get_data(cmd):
    try:
      return json_to_dict(run_cmd(cmd))
    except TasksError, e:
      raise KubeError(e)


class Pod(Kubectl):

  def __init__(self, name, namespace):
    """Initialize pod object

    Args:
      name (str): pod  name
      namespace (str): pod namespace

    Raises:
        KubeError: notify user of errors encoutered when running kubectl commands
    """

    super(Pod, self).__init__(name, namespace)

    try:
      self._data = Kubectl._get_data(
          "kubectl get po {0} -n {1} -o json".format(self.name, self.namespace))
      self.pvc_names = self._get_persistent_volume_claims()
    except TasksError as e:
      raise KubeError(e)

  def _get_persistent_volume_claims(self):
    result = {}
    for v in self._data['spec']['volumes']:
      if 'persistentVolumeClaim' in v:
        result[v['name']] = v['persistentVolumeClaim']['claimName']
    return result


class PersistentVolumeClaim(Kubectl):

  def __init__(self, name, namespace):
    """Initialize pvc object

    Args:
      name (str): pvc name
      namespace (str): pvc namespace

    Raises:
        KubeError: notify user of errors encoutered when running kubectl commands
    """

    super(PersistentVolumeClaim, self).__init__(name, namespace)

    try:
      self._data = Kubectl._get_data(
          "kubectl get pvc {0} -n {1} -o json".format(self.name, self.namespace))
      self.pv_name = self._get_persistent_volume()
    except TasksError as e:
      raise KubeError(e)

  def _get_persistent_volume(self):
    return self._data['spec']['volumeName']


class PersistentVolume(Kubectl):

  def __init__(self, name):
    """Initialize pvc object

    Args:
      name (str): pvc name

    Raises:
        KubeError: notify user of errors encoutered when running kubectl commands
    """

    self.name = name

    try:
      self._data = Kubectl._get_data(
          "kubectl get pv {} -o json".format(self.name))
    except TasksError as e:
      raise KubeError(e)

  def get_flex_volume_options(self):
    if 'flexVolume' in self._data['spec'].keys():
      return self._data['spec']['flexVolume']['options']

    return None

  def get_flex_volume_id(self, flex_volume_id_name):
    result = self.get_flex_volume_options()
    if result:
      if flex_volume_id_name in result.keys():
        return result[flex_volume_id_name]
    else:
      return result
