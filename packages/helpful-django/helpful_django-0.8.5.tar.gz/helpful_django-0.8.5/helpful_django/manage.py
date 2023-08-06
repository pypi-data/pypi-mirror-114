import sys

from utils.administrative import AdminCommandLine

cl = AdminCommandLine(
    argv=sys.argv
)
cl.run()
