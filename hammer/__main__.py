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
parser_bsv.add_argument('-n', '--namespace', default='default',
                        help='Pod namespace')
parser_bsv.add_argument('-a', '--pvc', default='home',
                        help='persistent volume claim name')


cli = parser.parse_args()


if cli.sub_cmd == 'get-bsv':
  try:
    pod = kube.Pod(cli.pod, cli.namespace)
  except kube.KubectlError as e:
    print(e.message)
    sys.exit(1)

  # if cli.verbose:
  #   print(pod.pvc_names)

  # Get PV for PVC home
  pvc_name = pod.pvc_names.get(cli.pvc)
  if pvc_name:
    pvc = kube.PersistentVolumeClaim(pvc_name, cli.namespace)
    pv = kube.PersistentVolume(pvc.pv_name)
    flex_volume_id = pv.get_flex_volume_id('BsvId')
    if flex_volume_id:
      print(flex_volume_id)
  else:
    print("No 'home' persistent volume claim")
    sys.exit(1)
