'''
Call this script from the command line as python delete_actionmenu.py 
***you MUST know the ID of the action menu you want to delete and enter it below

This is a very stupid script and is provided as a utility only


Documentation to come - note that you will have to write a find routine to find the
correct ID to delete!

Author Tom Stratton / tom at tomstratton dot net 
'''

from shotgun_api3 import Shotgun
from pprint import pprint

SERVER_PATH = 'https://*****.shotgunstudio.com' #your server path here
SCRIPT_USER = '********' #your script name 
SCRIPT_KEY =  '********' #your key here
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)
ID_TO_DELELE = 1
sg.delete('ActionMenuItem', ID_TO_DELELE)




# note that the id numbers will have to be either found or remembered!