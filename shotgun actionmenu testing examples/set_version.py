'''
What we are looking for, is a feature to create a playlist from within the shot list view ... 
we wanna have a ActionMenu script that can build a playlist of the selected shots and 
automatically look for a version based on one of the following :

1: A custom field we created under shots > current_version ... 
    in order to set the current version, we would also need a 
    ActionMenu script under the version page - where you can "Set as Current"

2: Newest version related to this shot

These to options should be two diffrent ActionMenu items (scripts)


    under the Version Detail Page - create a ActionMenu script called "Set as Current" - 
       - this should set/link the Current Version field, on the related/linked shot.

SAMPLE RESULTS FROM POST
    project_name Stereo Conversion Template 
    
    page_title Versions 
    
    entity_type Version 
    
    user_login tom 
    
    sort_column sg_task.Task.step 
    
    all_ids 19,20,93 
    
    selected_ids 19,20,93 
    
    sort_direction desc 
    
    user_id 52 
    
    project_id 64 
    
    column_display_names Version Name,Thumbnail,Link,Artist,Current Version2,Description,Status,Path to Frames,Uploaded Movie,Date Created 
    
    columns code,image,entity,user,sg_current_version2,description,sg_status_list,sg_path_to_frames,sg_uploaded_movie,created_at 
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

