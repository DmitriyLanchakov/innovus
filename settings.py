# encoding: utf-8
import glob
import os
from datetime import datetime


NOW = datetime.now()

rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
_ = lambda s: s

conffiles = glob.glob(rel('config', '*.conf'))
conffiles.sort()

for f in conffiles:
    execfile(f)
