#!/usr/bin/python

import concurrent.futures
import os
import requests
import sys
import time
import numpy as np

# Functions

def usage(status=0):
    progname = os.path.basename(sys.argv[0])
    print('''Usage: {} [-h HAMMERS -t THROWS] URL
    -h  HAMMERS     Number of hammers to utilize (1)
    -t  THROWS      Number of throws per hammer  (1)
    -v              Display verbose output
    '''.format(progname))
    sys.exit(status)

def hammer(url, throws, verbose, hid):
    ''' Hammer specified url by making multiple throws (ie. HTTP requests).

    - url:      URL to request
    - throws:   How many times to make the request
    - verbose:  Whether or not to display the text of the response
    - hid:      Unique hammer identifier

    Return the average elapsed time of all the throws.
    '''
    elapsed_time = 0
    total_throws = 0
    for throw in range(throws):
        start_time = time.time()
        request = requests.get(url)
        if verbose:
            print(request.text)
        throw_time = time.time() - start_time

        print("Hammer: {}, Throw: {:>3}, Elapsed Time: {:.2f}".format(hid, throw, throw_time))

        elapsed_time += throw_time
        total_throws += 1

    return elapsed_time / total_throws

def do_hammer(args):
    ''' Use args tuple to call `hammer` '''
    return hammer(*args)

def main():
    hammers = 1
    throws  = 1
    verbose = False
    
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        usage(1)

    # Parse command line arguments
    while len(arguments):
        argument = arguments.pop(0)

        if   argument == '-h':
            hammers = int(arguments.pop(0))
        elif argument == '-t':
            throws  = int(arguments.pop(0))
        elif argument == '-v':
            verbose = True
        elif argument.startswith('-') and len(argument) == 2:
            usage(1)
        else:
            url = argument 

    # Create pool of workers and perform throws
    average_time = []
    args = ((url, throws, verbose, hid) for hid in range(hammers))
    
    with concurrent.futures.ProcessPoolExecutor(hammers) as executor:
        average_time = list(executor.map(do_hammer, args))
    
    for hid in range(hammers):
        print("Hammer: {}, AVERAGE   , Elapsed Time: {:.2f}".format(hid, average_time[hid]))

    print("TOTAL AVERAGE ELAPSED TIME: {:.2f}".format(np.mean(average_time)))

# Main execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
