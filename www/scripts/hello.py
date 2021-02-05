#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

print('HTTP/1.0 200 OK')
print('Content-Type: text/html;charset=utf-8')
print('encoding: utf-8')
print()

form = cgi.FieldStorage()

print('''
<form>
    <input type="text" name="user" placeholder="Enter Name">
    <input type="submit" value="Say Hello">
</form>
''')

if 'user' in form:
    print('<h1>Hello, {}</h1>'.format(form['user'].value))
