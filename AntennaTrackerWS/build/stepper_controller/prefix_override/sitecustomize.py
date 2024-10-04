import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/blinn/Rocketry/antenna-tracker/AntennaTrackerWS/install/stepper_controller'
