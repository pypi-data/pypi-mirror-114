# -*- coding: utf-8 -*-
"""
__init__.py

Created on 2017-11-19 by hbldh <henrik.blidh@nedomkull.com>

"""
import pathlib
import logging
import sys
import os
import clr


logger = logging.getLogger(__name__)
_here = pathlib.Path(__file__).parent

# BleakUWPBridge
sys.path.append(str(pathlib.Path(__file__).parent))
clr.AddReference("BleakUWPBridge")


#dll_path=os.path.split(os.path.realpath(__file__))[0]

#sys.path.append(str(dll_path))
#clr.AddReference('BleakUWPBridge')

# install pythonnet
# try :
#    clr.AddReference('BleakUWPBridge')
# except:
#
#     print("please add BleakUWPBridge.ddl file ")
#     sys.exit()
    





# dll_path=os.path.split(os.path.realpath(__file__))[0]
# sys.path.append(str(dll_path))
#
#
# # install pythonnet
# try :
#    aiqi_blue=clr.AddReference("BleakUWPBridge")
# except:
#     print("please add BleakUWPBridge.ddl file ")
#     sys.exit()