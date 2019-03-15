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
    help='find block storage volume id for a given pvc',
    description=textwrap.dedent('''Description:
  Retrieve the BSV id in a PersistentVolume from target 
  PersistentVolumeClaim name (in a given namespace).

  By default the Kubernetes 'default' namespace is used.

      ''')
)
parser_bsv.add_argument('pvc', help='name of pvc')
parser_bsv.add_argument('-n', '--namespace', default='default',
                        help='Pod namespace')


cli = parser.parse_args()


def get_bsv_id(pvc, namespace):
  try:
    pvc = kube.PersistentVolumeClaim(pvc, namespace)
    pv = kube.PersistentVolume(pvc.pv_name)
    flex_volume_id = pv.get_flex_volume_id('BsvId')
    if flex_volume_id:
      return flex_volume_id
    else:
      print('No bsv found')
      sys.exit(1)
  except kube.KubectlError as e:
    print(e)
    sys.exit(1)


def main():

  if cli.sub_cmd == 'get-bsv':
    bsv_id = get_bsv_id(cli.pvc, cli.namespace)
    print(bsv_id)
