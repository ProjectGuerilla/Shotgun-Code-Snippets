'''

Documentation to come - note that you will have to write a find routine to find the correct
ID to delete!


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