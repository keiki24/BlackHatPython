#! /usr/bin/env python
# coding:utf-8

import Queue
import threading
import os
import urllib2

threads = 10

target = "https://www.test.com/"
dummy_directory = "/User/Me/Download/OpenSourceCode"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

web_paths = Queue.Queue()

for path, dirs, files in os.walk("."):
    for f in files:
        remote_path = "%s/%s" % (path, f)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(f)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)
        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            print "[%d] => %s" % (response.code, path)
            response.close()
        except urllib2.URLError as error:
            #print "Failed %s" % error.reason
            pass
        except urllib2.HTTPError as error:
            #print "Failed %s" % error.code
            pass

for i in range(threads):
    print "Spawing thread: %d" % i
    t = threading.Thread(target=test_remote)
    t.start()
