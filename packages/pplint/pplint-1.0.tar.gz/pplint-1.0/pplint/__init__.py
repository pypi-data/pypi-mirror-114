import sys

from pplint.cmd.init import Init
from pplint.cmd.analyze import analyze

if __name__ == '__main__':
    argv = sys.argv[1]
    if argv == '--init':
        init = Init()
    elif argv == '--analyze':
        analyze(sys.argv[1:])
