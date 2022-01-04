#!/usr/bin/python

import subprocess, getopt, sys


help = """
        startApp [OPTION] ... 
        \n\n-h, --help\t\t\tShow help
        \n-a, --application\t\t\tA list of software separated by coma(,)
        \n-m, --monitor\t\t\tThe number of the display the application will be running
"""

# Print the help information if an error occured and show the error
try:
    opts, args = getopt.getopt(sys.argv, "h:s:d", ["help", "application", "monitor"])
except getopt.GetoptError:
    print(help)
    print(getopt.GetoptError)

# Start the application
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(help)
        sys.exit()
    elif opt in ('-a', '--application'):
        pass
    elif opt in ('-m', '--monitor'):
        pass


subprocess.run(["discord", "&"])
subprocess.run(["spotify", "&"])


# https://github.com/calandoa/movescreen