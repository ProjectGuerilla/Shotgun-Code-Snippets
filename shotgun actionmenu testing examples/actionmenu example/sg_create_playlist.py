#!/usr/bin/python
# Version 0.2 - sets window to smaller size for better user experience

# Import modules for CGI handling 
import cgi, cgitb 
from pprint import pprint
import datetime

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
user_id = form.getvalue('user_id')
user_login  = form.getvalue('user_login')
title = form.getvalue('title')
entity_type = form.getvalue('entity_type')
cols = form.getvalue('cols')
column_display_names = form.getvalue('column_display_names')
sort_column = form.getvalue('sort_column')
sort_direction = form.getvalue('sort_direction')
selected_ids = form.getvalue('selected_ids')
ids = form.getvalue('ids')
project_name = form.getvalue('project_name')
project_id = form.getvalue('project_id')
now = datetime.datetime.now()

data_dict = { "user_id":user_id, 'user_login':user_login, 'title':title, 'entity_type':entity_type, 'cols':cols, 'column_display_names':column_display_names,
                'sort_column':sort_column, 'sort_direction':sort_direction, 'selected_ids':selected_ids, 'ids':ids, 'project_name':project_name, 'project_id':project_id, }

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
print '''<h2>You are about to create a playlist from the shots that you selected</h2>
Please enter a name and description for the playlist. <br/>Then click on Submit to complete the process<br />'''




# Feel free to edit the HTML above this line to make the form more beautiful...
# BUT DON'T MESS WITH THE CODE BETWEEN THESE COMMENT MARKERS!
print '<form name="input" action="sg_create_playlist_step_2.py" method="post">'

print '<em>Playlist Title:</em><br /><input type="text" name="playlist_title" size="100" value=%s /><br /><br />'% now.strftime('%b_%d_%H:%M:%S')

print '<em>Playlist Description:</em><br /><textarea rows="4" cols="80" name="playlist_description" > %s </textarea><br />' % 'Playlist Created by Actionmenu Script'
print '<input type="submit" value="Submit" />'

for key,value in data_dict.items():
    print '<input type="hidden" name="%s" value="%s"/>' % ( key, value)
# BUT DON'T MESS WITH THE CODE BETWEEN THESE COMMENT MARKERS!
# Feel free to edit the HTML below this line to make the form more beautiful...



print '</form>' 
print "</body>"
print "</html>"