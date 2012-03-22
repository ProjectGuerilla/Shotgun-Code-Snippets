'''
This is a very simple example of how to create a shotgun action menu item.
    run it from the command line with  - python create_actionmenu.py

To create the action menu you will have to fill in the information below:
    SERVER_PATH  - standard path to your shotgun db 
    SCRIPT_USER - the name of the script object you created in shotgun
    SCRIPT_KEY - the secret key from your script object
    URL_OF_CGI - the URL of the CGI handler script that is on a web server somewhere
    title - the name that will display in the action menu
    entity_type - what pages the action menu will show up on (eg: shot, version, playlist, etc.)
    selection_required - do you want the user to select some stuff (eg:shots) before
        the script can be run?


Author Tom Stratton / tom at tomstratton dot net  (code mostly stolen from SG docs)
'''

from shotgun_api3 import Shotgun
from pprint import pprint

SERVER_PATH = 'http://****.shotgunstudio.com' #your server path here
SCRIPT_USER = '*********' #your script name 
SCRIPT_KEY =  '*********' #your key here
URL_OF_CGI = "http://www.YOURURL.***/cgi-bin/set_current_version_posthandler_cgi.py"
title = "Set As Current Version"
entity_type = "Version"
selection_required = True



# initiate a shotgun API instance
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

#define the action menu item
data = {
  "title": title,
  "url": URL_OF_CGI,
  "list_order": 1,
  "entity_type": entity_type,
  "selection_required": selection_required, 

}

#Create the menu item
menu_item = sg.create("ActionMenuItem", data)
pprint(menu_item) # keep the output in case you need to delete the menu later!