#!/usr/bin/env python
import sys

if __name__ == '__main__':
    from .utils.administrative import AdminCommandLine
else:
    from helpful_django.utils.administrative import AdminCommandLine


def main():
    cl = AdminCommandLine(
        argv=sys.argv
    )
    cl.run()
