#!/usr/bin/python

# Import modules for CGI handling and shotgun API which must reside in same directory as this script
import cgi, cgitb 
from shotgun_api3 import Shotgun


# These values need to be set to fit with your environment
SERVER_PATH = 'https://****.shotgunstudio.com' #your server path here
SCRIPT_USER = '********' #your script name 
SCRIPT_KEY =  '********' #your key here
CURRENT_VERSION_FIELD = '********' # get this from the "Configure Field" dialog in shotgun

#set up fields variable to contain the Version fields that we want to retreive - 'entity' is the Link field which should link to a Shot 
#   NOTE - if any version is NOT linked to something via the entity field bad things will happen!
fields = ['id',  'entity', 'sg_asset_type'] # version id, shot info, "version"


#initialize shotgun
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

# Create instance of FieldStorage to process the POST data sent to this script 
form = cgi.FieldStorage() 

# Get data from fields 
selected_ids_str = form.getvalue('selected_ids')
form_project_id = form.getvalue('project_id')

# and convert to values that can be used by Shotgun API (list and ints)
version_ids=[int(x) for x in selected_ids_str.split(',')] # list of ints from a string
project_id =int(form_project_id)  # integer from string

# Boilerplate HTML - spice this up as necessary if you want to see a fancy display
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Set Current Version</title>"
print "</head>"
print "<body>"


# Wrap everything in an error catching routine so that we can attempt to show the user info about mistakes
try:
    print '<H1>Processing request to update shots to current versions...</H1>'
    print '</br>'
    print '</br>'
    success = True # keep track of errors so that true success for all requests can be reported to the user
    for a_version_id in version_ids:
        # want to find each Version that was sent to the POST request and handle it individually
        #   This might be able to run faster if I could have gotten id 'in' working but it always failed...
        filters = [
        ['project','is',{'type':'Project','id':project_id}],
        ['id', 'is', a_version_id ]
        ]
        
        #First get the version so that the linked shot can then be accessed.
        assets= sg.find("Version",filters,fields)

        if len(assets) < 1:
            print '</br>'
            print "<b>Shotgun Server Did Not Return Any Versions Matching %i </b>" % a_version_id
            print '</br>'
            print '</br>'            
            success = False

        else:
            
            for an_asset in assets: # go get the shot and update it with the Version info
            
                entity_type = an_asset['entity']['type'] # should always be 'Shot'!
                if entity_type == 'Shot': # we always expect a shot but OK to test
                    shot_id = an_asset['entity']['id']
                    linked_version = { 'type' : 'Version' , 'id' : a_version_id } 
                    data = { CURRENT_VERSION_FIELD : linked_version }
    
                    changed_asset = sg.update("Shot", shot_id, data) 
                    print 'Shot %i Has Been Updated Successfully' % shot_id     
                    print '</br>'     
                else:
                    success = False
                    print('version %s is linked to something other than a shot?' % a_version_id)
                    print '</br>'
    if success: #everything has gone well and the user gets a message
                    print '</br>'
                    print "<b>All requests successfully processed</b>"
                    print '</br>'

    print "</body>"
    print "</html>"


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

