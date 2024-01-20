#!/bin/env python

import json
import sys


'''
Description
-----------
This cripts converts the output of an Ansible dynamic inventory script to
static INI inventory.
Examples of usage
-----------------
./json2ini.py my_inventory.json
./dyn_script.sh | ./json2ini.py
./json2ini.py < my_inventory.json
'''


def usage(kind, text, rc=1):
    print("%s: %s\n" % (kind.upper(), text))

    print("Examples of usage:")
    print("  ./%s <filename> > hosts.ini" % sys.argv[0])
    print("  ./dyn_script.sh | ./%s > hosts.ini" % sys.argv[0])

    sys.exit(rc)


def main():
    if len(sys.argv) > 1:
        # Read data from file
        with open(sys.argv[1]) as f:
            data = json.load(f)
    elif not sys.stdin.isatty():
        # Read data from pipe
        data_in = sys.stdin.read()
        data = json.loads(data_in)
    else:
        usage("E", "No input data.")

    for k, v in data.items():
        if k == '_meta' and 'hostvars' in v:
            # Process hosts
            for host, h_vars in v['hostvars'].items():
                sys.stdout.write(host)

                for v_name, v_value in h_vars.items():
                    sys.stdout.write(" %s=%s" % (v_name, v_value))

                print("")
        else:
            kind = 'children'

            # Process groups
            if 'children' in v:
                print("[%s:children]" % k)
            elif 'hosts' in v:
                print("[%s]" % k)
                kind = 'hosts'

            for item in v[kind]:
                print(item)

            print()


if __name__ == '__main__':
    main()