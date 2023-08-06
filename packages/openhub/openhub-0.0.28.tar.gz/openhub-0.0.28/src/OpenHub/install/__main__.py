import os
from subprocess import call

os.chmod('install.sh', 755)
rc = call("./install.sh")