####################################################
# Copyright (c) 2013 Daniel Leblanc
#
# This program is released under the 'MIT License'. Please
# see the file COPYING in this distribution for license terms.
####################################################

from LovelyCorpus import *

import os
import sys

SEPERATE = "********************"
ALLTESTS = ["kfold", "setintrange", "entropygain"]

def runTests(tests = ALLTESTS):
    print SEPERATE
    print "Beginning tests"
    print SEPERATE
    if "kfold" in tests:
        print "---Testing kfold---"
        fname = "testFiles/1d/optdigits.data"
        print "1d tests"
        print "kfold with k = 10"
        print "original fname:", fname
        fnames = kfold(fname, 10)
        print "all files exist =",
        exists = True
        for f in fnames:
            exists = exists and os.path.exists(f)
        print exists
        print "Removing files..."
        for f in fnames:
            os.remove(f)
        try:
            fnames = kfold(fname, 1)
            print "---ERROR---"
        except AssertionError:
            print "Failed correctly for k=1"
        print SEPERATE
    if "setintrange" in tests:
        print "---Testing setintrange---"
        fname = "testFiles/1d/optdigits.data"
        print "Change range from 0-16 to 1-4"
        newname=fname+'.temp'
        setintrange(fname, 1, 4, newfname=newname)
        print "checking range"
        with open(newname) as f:
            count = 0
            for l in f:
                for d in l.split(',')[:-1]:
                    if int(d) > 4 or int(d) < 1:
                        count += 1
        print "---" + str(count) + " Val out of range---"
        os.remove(newname)
        print SEPERATE
    print "Finished"
    print SEPERATE

if __name__ == "__main__":
    if len(sys.argv) > 1:
        runTests(sys.argv[1:])
    else:
        runTests()
