import argparse
import sys
import textwrap
from . import __version__ as VERSION
from .actions import kube
from .utils import tasks
import constants

parser = argparse.ArgumentParser(
    prog='ducttape',
    description='A hacky utility tool to wrangle kubernetes and external cloud manager')

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=VERSION))

subparsers = parser.add_subparsers(
    dest='sub_cmd', title='sub commands', help='-h, --help', metavar='[sub-command]')

# bsv operations
parser_bsv = subparsers.add_parser(
    'get-bsv',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    help='find block storage volume id for a given pod',
    description=textwrap.dedent('''Description:
  Retrieve the PersistentVolume BSV id from a Pod name
  in a given namespace with a target PersistentVolumeClaim
  name.

  By default the Kubernetes 'default' namespace is used
  with PersistentVolumeClaim name 'home'.

      ''')
)
parser_bsv.add_argument('pod', help='name of pod')
parser_bsv.add_argument('-n', '--namespace', default='default',
                        help='Pod namespace')
parser_bsv.add_argument('-c', '--pvc', default='home',
                        help='persistent volume claim name')


cli = parser.parse_args()


def get_bsv_id():
  try:
    pod = kube.Pod(cli.pod, cli.namespace)
  except kube.KubectlError as e:
    print(e.message)
    sys.exit(1)

  # Get PV name for PVC name
  pvc_name = pod.pvc_names.get(cli.pvc)

  # Get block storage volume ID
  if pvc_name:
    pvc = kube.PersistentVolumeClaim(pvc_name, cli.namespace)
    pv = kube.PersistentVolume(pvc.pv_name)
    flex_volume_id = pv.get_flex_volume_id('BsvId')
    if flex_volume_id:
      return flex_volume_id
    else:
      print('No bsv found')
      sys.exit(1)
  else:
    print("No '{}' PersistentColumeClaim was found".format(cli.pvc))
    sys.exit(1)


def main():

  if cli.sub_cmd == 'get-bsv':
    bsv_id = get_bsv_id()

    # get host to validate tenancy details
    nodes = tasks.run_cmd("kubectl get nodes -o name")
    node = nodes.split('\n')[0]

    sub_tenancy = (node.split('/')[1])[1:5]

    print(tasks.run_cmd(
        "ecm -p {} bsv get {}".format(constants.ECM_PROFILES[sub_tenancy], bsv_id)))
