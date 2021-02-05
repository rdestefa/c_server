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
<h1>Markov Chain Simulator</h1>
<h2>Use the bottom two rows for absorbing states</h2>
<form>
   <input type="text" name="00" size="4">
   <input type="text" name="01" size="4">
   <input type="text" name="02" size="4">
   <input type="text" name="03" size="4">
   <input type="text" name="04" size="4">
   <br>
   <br>
   <input type="text" name="10" size="4">
   <input type="text" name="11" size="4">
   <input type="text" name="12" size="4">
   <input type="text" name="13" size="4">
   <input type="text" name="14" size="4">
   <br>
   <br>
   <input type="text" name="20" size="4">
   <input type="text" name="21" size="4">
   <input type="text" name="22" size="4">
   <input type="text" name="23" size="4">
   <input type="text" name="24" size="4">
   <br>
   <br>
   <input type="text" name="30" size="4">
   <input type="text" name="31" size="4">
   <input type="text" name="32" size="4">
   <input type="text" name="33" size="4">
   <input type="text" name="34" size="4">
   <br>
   <br>
   <input type="text" name="40" size="4">
   <input type="text" name="41" size="4">
   <input type="text" name="42" size="4">
   <input type="text" name="43" size="4">
   <input type="text" name="44" size="4">
   <br>
   <br>
   <input type="submit" value="Simulate Markov Chain">
</form>
''')

import numpy as np
import math

def mean_number_of_passages(Q, num_transient_states):
    return np.linalg.inv(np.subtract(np.identity(num_transient_states), Q))

def mean_time_to_absorption(W, num_transient_states):
    return W.dot(np.ones((num_transient_states, 1)))

def prob_of_absorption(W, R):
    return W.dot(R)

if len(form.keys()) == 25:
    if (float(form['00'].value) + float(form['01'].value) + float(form['02'].value) + float(form['03'].value) + float(form['04'].value) == 1) and (float(form['10'].value) + float(form['11'].value) + float(form['12'].value) + float(form['13'].value) + float(form['14'].value) == 1) and (float(form['20'].value) + float(form['21'].value) + float(form['22'].value) + float(form['23'].value) + float(form['24'].value) == 1) and (float(form['30'].value) + float(form['31'].value) + float(form['32'].value) + float(form['33'].value) + float(form['34'].value) == 1) and (float(form['40'].value) + float(form['41'].value) + float(form['42'].value) + float(form['43'].value) + float(form['44'].value) == 1):
        Q = np.array([[float(form['00'].value), float(form['01'].value), float(form['02'].value)],
                      [float(form['10'].value), float(form['11'].value), float(form['12'].value)],
                      [float(form['20'].value), float(form['21'].value), float(form['22'].value)]])
        R = np.array([[float(form['03'].value), float(form['04'].value)],
                      [float(form['13'].value), float(form['14'].value)],
                      [float(form['23'].value), float(form['24'].value)]])
    else:
        print('<h2>Rows do not add up to 1, using default matrix instead.</h2>')  
        Q = np.array([[float(0.2970), float(0.3960), float(0.0990)],
                      [float(0.1515), float(0.3030), float(0.3030)],
                      [float(0.1176), float(0.1176), float(0.1176)]])
        R = np.array([[float(0.1980), float(0.0100)],
                      [float(0.2273), float(0.0152)],
                      [float(0.5882), float(0.0590)]])
else:
    print('<h2>All boxes are not filled in, using default matrix instead.</h2>')
    Q = np.array([[float(0.2970), float(0.3960), float(0.0990)],
                  [float(0.1515), float(0.3030), float(0.3030)],
                  [float(0.1176), float(0.1176), float(0.1176) ]])
    R = np.array([[float(0.1980), float(0.0100)],
                  [float(0.2273), float(0.0152)],
                  [float(0.5882), float(0.0590) ]])

partA = mean_number_of_passages(Q, 3)
print('<h3>Mean number of passages over transient state j starting at transient state i:</h3>')
print('<p>{}</p>'.format(partA[0]))
print('<p>{}</p>'.format(partA[1]))
print('<p>{}</p>'.format(partA[2]))
partB = mean_time_to_absorption(partA, 3)
print('<h3>Mean time to absorption starting at transient state i:</h3>')
print('<p>{}</p>'.format(partB[0]))
print('<p>{}</p>'.format(partB[1]))
print('<p>{}</p>'.format(partB[2]))
partC = prob_of_absorption(partA, R)
print('<h3>Probability of absorption to absorbing state k:</h3>')
print('<p>{}</p>'.format(partC[0]))
print('<p>{}</p>'.format(partC[1]))
print('<p>{}</p>'.format(partC[2]))

