'''
Created on Mar 14, 2012

@author: tomstratton (tom at tomstratton.net)
tested with Python2.6
This script will run on a shotgun database, looking for users with skype user
names and inserting skype "call me" buttons if they are different or nonexistent.
It is designed to be run manually from time to time but could be adapted for event triggers

Some constants need to be provided before running this script:
    SERVER_PATH = 'https://******.shotgunstudio.com' #your server path here
    SCRIPT_USER = 'skype_button_adder' #your script name 
    SCRIPT_KEY =  '############' #your key here
    SKYPE_ID_FIELD = 'sg_skype_id' # the field name where the skype id is stored
    SKYPE_BUTTON_FIELD = 'sg_skype_button' # the field name where the skype button will reside
    
Instructions:
In shotgun you will need to create a script and get the name and script key.
    Put those into the varialbles below
Then you will need to have the following fields in your Users table:
    a field for the user's skype ID
    a field for the user's "Call Me"button to appear in
    a field for the user's "Add Me" skype button to appear in
    
    The names of those three fields should go into the appropriate variables below or use
    the names that are shows below when creating the field.
    
Run the script periodically, or via  a cron tast, or hook this up to an event trigger

'''
SERVER_PATH = 'https://XXXXX.shotgunstudio.com' #your server path here
SCRIPT_USER = 'XXXXXXXXX' #your script name 
SCRIPT_KEY =  '#########' #your key here
SKYPE_ID_FIELD = 'sg_skype_name'
SKYPE_BUTTON_FIELD = 'sg_skype_button'
SKYPE_ADD_CONTACT_FIELD = 'sg_add_skype_contact'

from shotgun_api3 import Shotgun
from pprint import pprint
import re
import string

#create template class that uses {{variable_name}} for replacement
class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''
# set up templates for the skype button    
button_template = MyTemplate('''<script type="text/javascript" src="http://download.skype.com/share/skypebuttons/js/skypeCheck.js"></script>
<a href="skype:{{skype_id}}?call"><img src="http://download.skype.com/share/skypebuttons/buttons/call_blue_white_124x52.png" style="border: none;" width="124" height="52" alt="Skype Me!" />''')
contact_template = MyTemplate('''<script type="text/javascript" src="http://download.skype.com/share/skypebuttons/js/skypeCheck.js"></script>
<a href="skype:{{skype_id}}?add"><img src="http://download.skype.com/share/skypebuttons/buttons/add_green_transparent_118x23.png" style="border: none;" width="118" height="23" alt="Add me to Skype" /></a>''')


#create a shotgun instance
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

#set up the data that we need for each user and look for non-blank skype id's
fields = ['id', SKYPE_ID_FIELD  , SKYPE_BUTTON_FIELD , SKYPE_ADD_CONTACT_FIELD] 
filters = [[SKYPE_ID_FIELD , 'is_not',  None ],]

#find all the users that have skype-id's
users= sg.find("HumanUser",filters,fields)

#initialize an empty list to contain shotgun update requests
batch_data = []

#process all users checking to see if button data is correct for the user name
# (this is in case a skype user name changes) or if there is not a button
for user in users:
    # put skype user name into template to create button html code
    skype_button_text = button_template.safe_substitute(skype_id=user[SKYPE_ID_FIELD])
    skype_contact_text = contact_template.safe_substitute(skype_id=user[SKYPE_ID_FIELD])
    
    if user[SKYPE_BUTTON_FIELD] <> skype_button_text:
        #set the skype button html into the user container
        user[SKYPE_BUTTON_FIELD] = skype_button_text
        user[SKYPE_ADD_CONTACT_FIELD] = skype_contact_text
        
        #remove extraneous data from user so that it can put into an update request 
        user_id = user.pop('id')
        dummy = user.pop('type')
        
        #append the update to the batch list
        batch_data.append( {'request_type':'update' , 'entity_type':'HumanUser' , 'entity_id': user_id , 'data':user})

# when done, process the updates to the users with a single call to shotgun (if necessary)
if batch_data:
    sg.batch(batch_data)
    
    