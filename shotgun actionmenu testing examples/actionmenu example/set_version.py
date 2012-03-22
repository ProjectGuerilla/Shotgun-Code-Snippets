'''
A hard coded script that I wrote as an intermediate step while writing
    a Shotgun API actionmenu handler.
    
It's probably not of much use to anyone but I don't see any reason to delete it yet,
    there are a LOT of hard coded values here so don't try and run this on your
    shotgun db. It's strictly a code sample.

Author Tom Stratton / tom at tomstratton dot net 
'''

from shotgun_api3 import Shotgun
from pprint import pprint

SERVER_PATH = 'https://****.shotgunstudio.com' #your server path here
SCRIPT_USER = '********' #your script name 
SCRIPT_KEY =  '********' #your key here
CURRENT_VERSION_FIELD = '********' # get this from the "Configure Field" dialog in shotgun
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)
fields = ['id',  'entity', 'sg_asset_type'] # version id, shot info, "version"

# sg_current_version field to upate

#TEST VALUES TO BE SET BY POST FROM ACTION MENU
version_ids = [19, 20, 93] # replace with result from the post
project_id =64  # Replace this with the result from the post



for a_version_id in version_ids:
    filters = [
    ['project','is',{'type':'Project','id':project_id}],
    ['id', 'is', a_version_id ]
    ]
    assets= sg.find("Version",filters,fields)
    if len(assets) < 1:
        print "couldn't find any assets"
        exit(0)
    else:
        for an_asset in assets:
            entity_type = an_asset['entity']['type'] # should always be 'Shot'!
            if entity_type == 'Shot': # we always expect a shot but OK to test
                shot_id = an_asset['entity']['id']
                linked_version = { 'type' : 'Version' , 'id' : a_version_id } 
                data = { CURRENT_VERSION_FIELD : linked_version }

                changed_asset = sg.update("Shot", shot_id, data) 
                pprint(changed_asset)           
            else:
                print('version %s is linked to something other than a shot?' % a_version_id)

