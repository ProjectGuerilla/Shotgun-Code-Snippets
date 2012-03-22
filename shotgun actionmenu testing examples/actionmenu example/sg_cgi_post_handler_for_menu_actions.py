#!/usr/bin/python
# note - you may have a different path to python on your server! - 
'''
This is a basic post request handler that can be run after you are sure that
you are able to run python scripts as cgi.

It can be set as the target of a Shotgun API action menu and will simply print out 
    all of the information that is sent to the server by shotgun. It can also be useful
    when debugging or as a stub for writing your own handler/
    
Author Tom Stratton / tom at tomstratton dot net    
'''

# Import modules for CGI handling 
import cgi, cgitb 
from pprint import pprint

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
user_id = form.getvalue('user_id')
user_login  = form.getvalue('user_login')
page_title = form.getvalue('title')
entity_type = form.getvalue('entity_type')
columns = form.getvalue('cols')
column_display_names = form.getvalue('column_display_names')
sort_column = form.getvalue('sort_column')
sort_direction = form.getvalue('sort_direction')
selected_ids = form.getvalue('selected_ids')
all_ids = form.getvalue('ids')
project_name = form.getvalue('project_name')
project_id = form.getvalue('project_id')

data_dict = { "user_id":user_id, 'user_login':user_login, 'page_title':page_title, 'entity_type':entity_type, 'columns':columns, 'column_display_names':column_display_names,
                'sort_column':sort_column, 'sort_direction':sort_direction, 'selected_ids':selected_ids, 'all_ids':all_ids, 'project_name':project_name, 'project_id':project_id, }

notes_from_shotgun_docs = '''

POST contents
User data
user_id: The user id of the currently logged in user (eg: 34)
user_login: The login of the currently logged in user (eg: joe)
Page data
title: The page title (eg. "All Versions")
entity_type: The entity type of the current page (eg. Version)
cols: A comma-separated list of system field names of all the visible columns on the page (eg. code, sg_status_list, description)
column_display_names: A comma-separated list of display names of all the visible columns on the page (eg. Version, Status, Description)
sort_column: The system name of the column that was sorted by (eg. code). 
     * Only sent if there is a sort applied. If an advanced sort is applied, only the first sort-by column is sent. 
sort_direction: (eg. asc or desc)
     * Only sent if there is a sort applied 
Entity Ids
selected_ids: A comma-separated list of the selected entity ids (eg: 931, 900)
ids: A comma-separated list of all ids of the entities returned by the current page's query. This returns ALL Ids, including those that aren't visible due to pagination. (eg: 931, 900, 904, 907)
Project data (only sent if all entities on the current page share the same project)
project_name: The name of the Project (eg: Gunslinger)
project_id: The Id of the Project (eg: 81)
'''

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"

for key,value in data_dict.items():
    print key, value
    print "</br></br>"

print "</body>"
print "</html>"