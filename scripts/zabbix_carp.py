import sys
import subprocess
from subprocess import run
import re

IFCONFIG_OUTPUT = run(['ifconfig', '-a'], capture_output=True).stdout.decode('utf-8')

def parseOutput():
    payload = []
    re_start = re.compile('([a-z0-9\.]+): flags=.+metric.+mtu.+')
    re_desc = re.compile('description: (.+)')
    re_carp = re.compile('carp: (.+) vhid (\d+)')
    interfaces = []
    temp = None
    lines = IFCONFIG_OUTPUT.split('\n')
    for line in lines:
        match = re.search(re_start, line)
        if match:
            if temp is not None:
                interfaces.append(temp)
            temp = {}
            temp['name'] = match.group(1)
            temp['desc'] = ''
            temp['carp'] = []
            continue
        match = re.search(re_desc, line)
        if match and temp is not None:
            temp['desc'] = match.group(1)
            continue
        match = re.search(re_carp, line)
        if match and temp is not None:
            carp = {}
            carp['vhid'] = match.group(2)
            carp['status'] = match.group(1)
            temp['carp'].append(carp)
            continue
    if temp is not None:
        interfaces.append(temp)
    template = '{{"{{#INTERFACE}}":"{0}","{{#DESCRIPTION}}":"{1}","{{#VHID}}":"{2}"}}'
    for interface in interfaces:
        if (interface['carp']):
            for carp in interface['carp']:
                payload.append(template.format(interface['name'], interface['desc'], carp['vhid']))
    return '[' + ','.join(payload) + ']'

if __name__ == "__main__":
    out = parseOutput()
    sys.exit(out)
