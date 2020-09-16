import argparse
from argparse import RawTextHelpFormatter

# Redefines argparse's default usage/help prefix
class HelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = ''
        return super(HelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

def parse_args():
  ''' Defines arguments '''
  
  # Custom usage/help
  main_args = """
  Usage: 
    python getdc.py -d contoso.local
    python getdc.py -d contoso-a.local constoso-b.local 
    python getdc.py -d contoso.local -n 8.8.8.8
    python getdc.py -d contoso.local -n ns1.contoso.local
    python getdc.py -d contoso.local -n ns1.contoso.local -f host

  Required arguments:
    [-d, --domain] define domain, accepted values 'hostname', 'hostnames(seperate by a space)'

  Optional arguments:
    [-n, --nameserver] define nameserver, accepted values 'hostname', 'ipaddress'
    [-f, --format] format output type, accepted values 'json(default)', 'host', 'ip' 'hostip'
    [-v, --verbose] toggle debug meesages to stdout
    [-e, --exchange] additionally retrieve exchange hosts
  """
  # Define parser
  parser = argparse.ArgumentParser(formatter_class=HelpFormatter, description='', usage=main_args, add_help=False)
  # Main argument group
  main_group = parser.add_argument_group('main_args')
  main_group.add_argument('-d', '--domain', required=True, type=str, metavar='', default='', help='Domain required', nargs='+')
  main_group.add_argument('-n', '--nameserver', required=False, type=str, metavar='', default='', help='Define Nameserver')
  main_group.add_argument('-f', '--format', required=False, type=str, default='json', choices=['json', 'host', 'ip', 'hostip'])  
  main_group.add_argument('-e', '--exchange', required=False, action='store_false')
  # Mutually Exclusive group
  mutually_exclusive_group = parser.add_mutually_exclusive_group()
  mutually_exclusive_group.add_argument('-v', '--verbose', action='store_true')
 
  # Initiate parser instance
  args = parser.parse_args()
  return args

def main():
  import arguments
  arguments.parse_args()

if __name__ == "__main__":
    main()
