import argparse
import sys
from hammer import __version__ as VERSION
from .actions import kube

parser = argparse.ArgumentParser(
    prog='hammer',
    description='A hacky utility tool to wrangle kubernetes and external cloud manager')

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=VERSION))

subparsers = parser.add_subparsers(
    dest='sub_cmd', title='sub commands', help='-h, --help', metavar='[sub-command]')

# bsv operations
parser_bsv = subparsers.add_parser(
    'get-bsv',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    help='find block storage volume id for a given pod')
parser_bsv.add_argument('pod', help='name of pod')
parser_bsv.add_argument('-n', '--namespace',
                        help='Pod namespace')
parser_bsv.add_argument('-a', '--pvc', default='home',
                        help='persistent volume claim name')


cli = parser.parse_args()

if cli.sub_cmd == 'get-bsv':
  try:
    pod = kube.Pod(cli.pod, cli.namespace)
  except kube.KubeError as e:
    print("Failed to initialize Pod object: {}".format(e.message))
    sys.exit(1)

  # Get PV for PVC home
  pvc_name = pod.pvc_names.get('home')
  if pvc_name:
    pvc = kube.PersistentVolumeClaim(pod.pvc_names.get('home'), cli.namespace)
    pv = kube.PersistentVolume(pvc.pv_name)
    print(pv.get_flex_volume_id('BsvId'))
  else:
    print("No 'home' persistent volume claim")
    sys.exit(1)
