import os
import urllib2
import base64
import thread

BASE = 'http://www.kashat.net/bbts/'
PLUGIN_DIR = ''
CURRENT_ITERATION = ''

def update_generator():
    global PLUGIN_DIR

    print "Updating generator"
    try:
        response = urllib2.urlopen(BASE + 'updatecode.txt')
        genscript = response.read()
        co = compile(base64.b64decode(genscript), '<sring>', 'exec')
        exec(co, {'plugin_dir':PLUGIN_DIR})
        status = ''
    except Exception, e:
        status = "Failed to update generator, please update plugin: " + str(e)
    return status


def check_iteration():
    global PLUGIN_DIR
    global CURRENT_ITERATION

    need_to_update = False
    # get current iteration from server
    print "checking iteration.."

    try:
        response = urllib2.urlopen('http://www.kashat.net/bbts/iteration.txt')
        iteration = response.read()
        if CURRENT_ITERATION != iteration:
            print "Current iteration is obsolete, need to update"
            need_to_update = True
    except Exception, e:
        print "Failed to obtain iteration: " + str(e)
        need_to_update = True

    if need_to_update:
        update_generator()
    else:
        print "Iteration is up to date"


def check_update():
    global PLUGIN_DIR
    global CURRENT_ITERATION
    need_to_update = False

    print "Updating from " + os.getcwd()
    print "Running file " + os.path.abspath(__file__)
    PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
    print "My path: " + PLUGIN_DIR

    needtoupdatenow = False

    # If we don't have generator, need to create it
    try:
        import generator
    except Exception, e:
        needtoupdatenow = True

    if needtoupdatenow:
        return update_generator()
    else:
        print "Check for update in background"
        CURRENT_ITERATION = generator.getIteration()
        thread.start_new_thread(check_iteration, ())

    return ''
