#!/usr/bin/python
'''
This is a cgi handler for a shotgun action menu item. It must reside on a web server
    which is able to run python cgi scripts. In general, it is *not* on the same server
    that hosts your shotgun database.
    
Specifically, this is a script that enables someone to call an action menu from a version
    and that version will automatically update it's associated shot so that the "current 
    version field" in the shot table points to the version selected before calling the
    action menu. If more than one version is selected then all associated shots will be 
    updated.
    
The URL of this script needs to be coded into your action menu item - see:
    create_actionmenu.py for more info. You will need to put the shotgun_api3 folder in 
    the same location as this script (on the server).
    
This is Version 0.2 of this handler - integrating an external config file for server info
    and all the HTML has been put into variables for ease of editing.

NOTE: You MUST set variables in this script pointing to your config file!
    
Author Tom Stratton / tom at tomstratton dot net
'''
# These variables MUST be set by the script user! The config file referenced here has more information that 
#   should be entered in it as well
CONFIG_FILE = 'sgkeys.cfg'                     #config file assumed in same directory as script
THIS_SCRIPT_CONFIG = 'set_current_version'  # the config file section used by this script  - this allows the same config file to be shared by multiple scripts     


# Editable HTML OUTPUT STRINGS FOLLOWS
HEADER_HTML = '''<html>
    <head>
    <title>Set Current Version</title>
    <script>
       function changeScreenSize(w,h)
         {
           window.resizeTo( w,h )
         }
    </script>
    </head>
    <body onload="changeScreenSize(500,500)">
    <H1>Processing request to update shots to current versions...</H1>
    </br>
    </br>
    '''
EXCEPTION_HTML = '''
    Something Drastic Has Gone Wrong!</br>
    Check that all versions are linked to shots</br>
    The following message MAY shed some light on it...</br>
    %s
    <form method="post">
    <input type="button" value="Close Window" 
    onclick="window.close()">
    </form>
    '''
MULTISHOT_ERROR_HTML = '''
    %s
    <h2>None of your request has been processed</h2>
    <form method="post">
    <input type="button" value="Close Window" 
    onclick="window.close()">
    </form>   
    '''    
CONFIG_ERROR_HTML = '''
    The configuration file needed to access shotgun is missing or invalid.</br>
    Please consult your shotgun administrator
    '''
SUCCESS_MESSAGE_HTML = '''
    </br>
    <b>All requests successfully processed</b>
    </br> Window will close monetarily</br>
    <SCRIPT LANGUAGE="JavaScript"><!--
    setTimeout('self.close()',500);
    //--></SCRIPT>
    '''    
CLOSING_HTML = '''
    </br>
    </body>
    </html>
    '''
# Feel free to alter the HTML above this line - %s is a replacement string that will get filled in by the code

print "Content-type:text/html\r\n\r\n"  # the magic line needs to be exactly like this - do not edit.
print HEADER_HTML

class MultiShotError(Exception):
   def __init__(self, value):
       self.message = value
   def __str__(self):
       return repr(self.message)
       
class ConfigError(Exception):
   def __init__(self, value):
       self.message = value
   def __str__(self):
       return repr(self.message)

#whole script wrapped in a try handler so that I can see useful error messages if there is a crash!
try:
    # Import modules for CGI handling and shotgun API which must reside in same directory as this script
    import cgi
    import cgitb 
    from pprint import pprint
    from shotgun_api3 import Shotgun
    from pprint import pprint
    from os import path
    import ConfigParser
    import datetime
    import urllib
    import time

    # #mark Load Config Data
    if path.isfile(CONFIG_FILE): #test for existence of config file
        config = ConfigParser.RawConfigParser()
        config.read(CONFIG_FILE)
        SERVER_PATH = config.get( THIS_SCRIPT_CONFIG, 'SERVER_PATH')
        SCRIPT_USER = config.get( THIS_SCRIPT_CONFIG,'SCRIPT_USER')
        SCRIPT_KEY = config.get( THIS_SCRIPT_CONFIG,'SCRIPT_KEY')
        CURRENT_VERSION_FIELD = config.get( THIS_SCRIPT_CONFIG, 'CURRENT_VERSION_FIELD')
    else:
        raise ConfigError('Your server side configuration file is missing!')

    #set up fields variable to contain the Version fields that we want to retreive - 'entity' is the Link field which should link to a Shot 
    #   NOTE - if any version is NOT linked to something via the entity field bad things will happen!
    fields = ['id',  'entity', 'sg_asset_type', ] # version id, shot info, "version"
    
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

    success = True # keep track of errors so that true success for all requests can be reported to the user
    filters = [
        ['project','is',{'type':'Project','id':project_id}],
        ['id', 'in' ] + version_ids ,
        ]
    versions= sg.find("Version",filters,fields)
    found_shots = set() # a set to hold all of the found shots so we can error if we need to...

    for a_version in versions: #pre-process all shots looking for duplicates
        print "</br>"
        if a_version['entity']['name'] in found_shots:
            raise MultiShotError(
                'There is more than one version of shot %s in your request' % a_version['entity']['name'] )
        else:
            found_shots.add( a_version['entity']['name'] )

    for a_version in versions: # re-process all shots to set the current version field correctly           
        entity_type = a_version['entity']['type'] # should always be 'Shot'!
        if entity_type == 'Shot': # we always expect a shot but OK to test
            shot_id = a_version['entity']['id']
            linked_version = { 'type' : 'Version' , 'id' : a_version['id'] } 
            data = { CURRENT_VERSION_FIELD : linked_version }
            changed_asset = sg.update("Shot", shot_id, data) 
            print 'Shot %i Has Been Updated Successfully' % shot_id     
            print '</br>'     

        else:
            success = False
            print('version %s is linked to something other than a shot?' % a_version_id)
            print '</br>'
            
    if success: #everything has gone well and the user gets a message
        print SUCCESS_MESSAGE_HTML

except ConfigError, (errmsg):
    print CONFIG_ERROR_HTML

except MultiShotError, (errmsg):
    print MULTISHOT_ERROR_HTML % errmsg

except Exception, errmsg:
    print EXCEPTION_HTML  % errmsg
    
#Always close the html tags! - YOU CAN EDIT ANY HTML BELOW THIS LINE IT WILL ALWAYS APPEAR
print CLOSING_HTML

