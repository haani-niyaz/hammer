import json
from .utils.tasks import run_cmd


def main():

  # Find PVC from Pod
  pod = json.loads(run_cmd('kubectl get po jira-0 -n proteus -o json'))
  for volume in pod['spec']['volumes']:

    # Explicitly looking for home
    if volume['name'] == 'home':
      pod_volume = volume['persistentVolumeClaim']['claimName']

  # Find PV from PVC
  pvc = json.loads(
      run_cmd("kubectl get pvc {} -n proteus -o json".format(pod_volume)))

  pv_name = pvc['spec']['volumeName']

  # Get BSV ID from PV
  pv = json.loads(run_cmd("kubectl get pv {} -o json".format(pv_name)))

  # Explicitly looking for a flexVolume
  # if 'flexVolume' in pv['spec'].keys() and 'BsvId' in pv['spec']['flexVolume']['options'].keys():
  #   bsv_id = pv['spec']['flexVolume']['options']['BsvId']

  #   # Get bsv details from ecm
  #   print(bsv_id)
  #   bsv = json.loads(run_cmd('ecm -p p-pro-pro bsv get {}'.format(bsv_id)))
  #   print(bsv)

  site = run_cmd(
      'kubectl get nodes -n proteus -o name').split('\n')[0].split('/')[1]
  print(site)
