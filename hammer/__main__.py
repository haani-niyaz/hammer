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
    'bsv',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    help='find block storage volume details for a given pod')
parser_bsv.add_argument('name', help='name of pod')
parser_bsv.add_argument('-n', '--namespace',
                        help='Pod namespace')
parser_bsv.add_argument('-v', '--verbose',
                        help='show detailed output')


cli = parser.parse_args()

if cli.sub_cmd == 'bsv':
  try:
    pod = kube.Pod(cli.name, cli.namespace)
  except kube.KubeError as e:
    print("Failed to initialize Pod object: {}".format(e.message))
    sys.exit(1)

  print(pod.pvcs)
