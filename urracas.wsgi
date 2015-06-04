activate_this = 'C:\\AppServ\\www\\env\\Scripts\\activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, "C:\\AppServ\\www\\")

from urracas import app as application
