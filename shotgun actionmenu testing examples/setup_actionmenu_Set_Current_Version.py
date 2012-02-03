'''

Docuemntation to come

'''

from shotgun_api3 import Shotgun
from pprint import pprint

SERVER_PATH = 'http://****.shotgunstudio.com' #your server path here
SCRIPT_USER = '*********' #your script name 
SCRIPT_KEY =  '*********' #your key here
URL_OF_CGI = "http://www.YOURURL.***/cgi-bin/set_current_version_posthandler_cgi.py"
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

data = {
  "title":"Set As Current Version",
  "url": URL_OF_CGI,
  "list_order": 1,
  "entity_type": "Version",
  "selection_required": True, 

}

#Create the menu item
menu_item = sg.create("ActionMenuItem", data)