#!/usr/bin/python
# Version 0.2 Sets window to smaller size and redirects back to shotgun (closing data entry window) when complete
# #mark GLOBAL VARIABLES TO BE SET BY END USER

#   using a config file to make it easier to share scripts without revealing private information
CONFIG_FILE = 'sgkeys.cfg'                     #config file assumed in same directory as script
THIS_SCRIPT_CONFIG = 'create_playlist'  # the config file section used by this script  - this allows the same config file to be shared by multiple scripts     

# Editable HTML OUTPUT FOLLOWS

# Feel free to alter the HTML of this script between here and the next tag like this!VVVVVVVVVVVVV

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Creating Playlist From Shots</title>"
print """<script>
   function changeScreenSize(w,h)
     {
       window.resizeTo( w,h )
     }
</script> """
print "</head>"
print '<body><body onload="changeScreenSize(700,350)">'



# Feel free to alter the HTML of this script between here and the LAST tag like this! ^^^^^^^^^^^^







# Import modules for CGI handling, shotgun and other script requirements 
import cgi, cgitb 
from pprint import pprint
from shotgun_api3 import Shotgun
from pprint import pprint
from os import path
import ConfigParser
import datetime
import urllib
import time

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields (this data sent by shotgun)
selected_ids_str = form.getvalue('selected_ids')                          # the id's of all the shots that were selected when the script was called AS A STRING
form_project_id = form.getvalue('project_id')                             # The project ID of the project the script was called from as a string value
form_user_id = form.getvalue('user_id')                                     # The STRING user id of the person calling the script - will get assigned to the playlist

# Get data from fields (this data entered by user)
playlist_name = form.getvalue('playlist_title')                              # The name of the playlist that will get created
playlist_description = form.getvalue('playlist_description')           # The description of the playlist that will get created

# Convert values so that they can be used by Shotgun API (list and ints)
shot_ids=[int(x) for x in selected_ids_str.split(',')] # list of ints from a string   - this is the list of shot ID's that will be used to generate the playlist
PROJECT_ID = int(form_project_id)                                                    # The project ID of the project the script was called from - make an integer from string
script_user_id = int(form_user_id)                                                      # The INTEGER user id of the person calling the script - will get assigned to the playlist


# #mark Load Config Data
if path.isfile(CONFIG_FILE): #test for existence of config file
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    SERVER_PATH = config.get( THIS_SCRIPT_CONFIG, 'SERVER_PATH')
    SCRIPT_USER = config.get( THIS_SCRIPT_CONFIG,'SCRIPT_USER')
    SCRIPT_KEY = config.get( THIS_SCRIPT_CONFIG,'SCRIPT_KEY')
    CURRENT_VERSION_FIELD = config.get( THIS_SCRIPT_CONFIG, 'CURRENT_VERSION_FIELD')
    PLAYLIST_STATUS = config.get( THIS_SCRIPT_CONFIG, 'PLAYLIST_STATUS')
    PLAYLIST_TYPE  = config.get( THIS_SCRIPT_CONFIG, 'PLAYLIST_TYPE')

# #mark Set Up Additional Variables/Containers
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)
version_ids=[] # start with an empty list and then add to it as we get information
now = datetime.datetime.now()
shot_fields = ['id',  'entity', 'sg_asset_type',  CURRENT_VERSION_FIELD] # version id, shot info, "version"
version_fields = ['id', 'entity']




try:
    print '<h3>Processing request to create playlist from current version of these shots...</h3>'
    print '</br>'
    print '</br>'
    success = True # keep track of errors so that true success for all requests can be reported to the user
    
       
    shot_filters = [
    ['project','is',{'type':'Project','id':PROJECT_ID}],
    ['id', 'in', ] + shot_ids
    ]
    
    # #mark First get the version so that the linked shot can then be accessed.
    assets= sg.find("Shot", shot_filters, shot_fields)

    # did anything get returned? if not then error out...
    if len(assets) < 1:
        print '</br>'
        print "<b>Shotgun Server Did Not Return Any Shots! </b>"
        print '</br>'
        print '</br>'            
        success = False


    else: # something was returned, process it!
                        
        for an_asset in assets: # get the appropriate version and append it to the version list
            
             # first, look to see if there is a current version in the shot data
            if an_asset[CURRENT_VERSION_FIELD]: # there is a valid version in the field, append it to the list:
                version_ids.append(an_asset[CURRENT_VERSION_FIELD]['id']) # put the returned asset id onto the list
            
            else : # if not, then find all the versions that link to that shot and return the most recent
                order_by_date = [{'field_name':'created_at','direction':'desc'}, ] # order the output of the find by creation date - MUST be a list of dicts!
                linked_shot = { 'type' : 'Shot' , 'id' : an_asset['id']} # get the id from the current asset we are looking at and use it to create a shot dict
                version_filters = [
                                ['project','is',{'type':'Project','id':PROJECT_ID}],
                                ['entity', 'is', linked_shot ] 
                                ]
                linked_versions = sg.find('Version', version_filters, version_fields,order_by_date)
                version_ids.append(linked_versions[0]['id']) # use zero index to get the most recent version linked to the shot because of sort order
        
        # a list of version ID's has been generated and the new playlist can now be constructed
        playlist_user = {'type' : 'HumanUser' , 'id' : script_user_id}
        versions_list = [ {'type' : 'Version', 'id' : x } for x in version_ids ]
        data = {
            'project': { 'type' : 'Project' , 'id' : PROJECT_ID } ,
            'code' : playlist_name ,
            'description' : playlist_description ,
            'sg_status' : PLAYLIST_STATUS ,
            'versions' : versions_list ,
            'sg_type' : PLAYLIST_TYPE ,
            'sg_script_user' : playlist_user ,
            'sg_date_and_time' : now
            }
        
        
        #Create the Playlist in Shotgun
        playlist = sg.create("Playlist",data)

        if not playlist : #error! nothing came back from SG!
            success = False

    if success: #everything has gone well and the user gets a message
                    print '</br>'
                    print "<b>Playlist successfully created</b>"
                    path_to_playlist = SERVER_PATH + '/detail/Playlist/' + str(playlist['id'])
                    #print '<a href="%s">Visit Playlist Now</a>' % path_to_playlist 
                    #print '</br>Will redirect automatically in 5 seconds'
                    print '''<a href="#" onclick="window.opener.location.href='%s'; window.opener='x';window.close();">Visit Playlist Now</a>''' % path_to_playlist
                    #print'<meta http-equiv="REFRESH" content="3;url=%s">' % path_to_playlist
                    print '</br>'

    print "</body>"
    print "</html>"

#https://guerilla.shotgunstudio.com/page/1378#Feb_20_18%3A11%3A34
#https://guerilla.shotgunstudio.com/page/1378#Playlist_22_Feb_20_18%3A11%3A34

except Exception, e:
    print "Something Drastic Has Gone Wrong!"
    print '</br>'
    print "Check that all versions are linked to shots"
    print '</br>'
    print "The following message MAY shed some light on it..."
    print '</br>'
    print "%s" % e
    print '</br>'
    print "</body>"
    print "</html>"
