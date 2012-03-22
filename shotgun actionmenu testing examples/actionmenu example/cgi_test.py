#!/usr/bin/python
'''
This is a minimal cgi script that can be used to test a web server to make sure
    that you are able to serve cgi scripts. 
    
    These are the issues that can be tested with this script:
    
    On shared hosts you many need to put cgi scripts in the cgi-bin folder 
        or set up a custom .htaccess file.
    
    Note that you may need to save this as a .cgi file instead of .py for some server
        configureations
    
    Also, you may need a different #! line at the top of the script to run it on your 
        server as well
        
Author Tom Stratton / tom at tomstratton dot net (code stolen from Stack Overflow)
'''
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
</body>

</html>
""" % cgi.escape(message)