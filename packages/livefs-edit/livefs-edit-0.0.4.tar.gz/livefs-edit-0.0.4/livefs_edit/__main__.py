#!/usr/bin/python3

import sys

import yaml

from livefs_edit import cli
from livefs_edit.context import EditContext
from livefs_edit.actions import ACTIONS


HELP_TXT = """
# livefs-edit source.iso dest.sio [actions]

livefs-edit makes modifications to Ubuntu live ISOs.

Actions include:

 * --setup-rootfs
 * --shell
 * --cp
 * --inject-snap
 * --edit-squashfs
 * --add-cmdline-arg
 * --add-autoinstall-config
 * --add-debs-to-pool
 * --add-packages-to-pool
 * --unpack-initrd

"""


def main(argv):
    if '--help' in argv:
        print(HELP_TXT)
        sys.exit(0)

    isopath = argv[0]
    destpath = argv[1]
    if destpath == '/dev/null':
        destpath = None

    ctxt = EditContext(isopath)
    ctxt.mount_iso()

    if argv[2] == '--action-yaml':
        calls = []
        with open(argv[3]) as fp:
            spec = yaml.load(fp)
        print(spec)
        for action in spec:
            func = ACTIONS[action.pop('name')]
            calls.append((func, action))
    else:
        try:
            calls = cli.parse(ACTIONS, argv[2:])
        except cli.ArgException as e:
            print("parsing actions from command line failed:", e)
            sys.exit(1)

    try:
        for func, kw in calls:
            print(
                "running", func.__name__.replace('_', '-'),
                "with arguments", kw)
            func(ctxt, **kw)

        if destpath is not None:
            ctxt.repack_iso(destpath)
    finally:
        ctxt.teardown()


if __name__ == '__main__':
    main(sys.argv[1:])
