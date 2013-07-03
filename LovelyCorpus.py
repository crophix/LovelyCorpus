####################################################
# Copyright (c) 2013 Daniel Leblanc
#
# This program is released under the 'MIT License'. Please
# see the file COPYING in this distribution for license terms.
####################################################

import sys
import random
from types import *

FIRST = 0
LAST = -1

def setintrange(fname, mn, mx, clposition=LAST, attr=[]):
    """
    Change attributes so that they fall within the given range.

    All attributes are changed to fall within the range. The range is
    defined as inclusive of the min and max values provided.
    i.e. [mn, mx]. The index of the classifier for each entry is stored
    in the clposition variable.  If only certain attributes should be 
    changes a list of indices can be included in the attr variable.
    """
    assert type(mn) is IntType
    assert type(mx) is IntType
    assert type(clposition) is IntType
    assert type(attr) is ListType
    assert mn < mx
    try: 
        data = []
        with open(fname) as f:
            data.append(f.readline())
    except IOError:
        print "Invalid filename"
        return
    data = [data[x].split(',') for x in range(len(data))]
    if attr == []:
        attr = range(len(data[0]))
        attr.pop(clposition)
    curMax = mx
    curMin = mn
    for i in range(len(data)):
        for a in attr:
            curMax = max(data[i][a], curMax)
            curMin = min(data[i][a], curMin)
    div = mx - mn + 1
    for i in range(len(data)):
        for a in attr:
            data[i][a] = mn + (data[i][a]/div)
    return

def kfold(fname, k):
    """
    Creates 'k' training files and 'k' test files.

    The file reference by 'fname' should be in the standard formatting 
    referenced in the documentation.  The names of the training and test
    files will be based on the provided 'fname'.  A list of filenames will 
    be returned.
    """
    assert type(k) is IntType
    assert k > 1
    try:
        data = []
        with open(fname) as f:
            data.append(f.readline())
    except IOError:
        print "Invalid filename"
        return
    rname = fname.splot('.')[0]
    foldsize = len(data) / k + 1
    unused = list(data)
    names = []
    for i in range(k):
        if i == k-1:
            test = unused
        else:
            test = []
            for j in range(foldsize):
                item = unused.pop(random.randrange(len(unused))
                test.append(item)
        name = rname + str(i)
        names.append(name+'.train')
        with open(name+'.train', 'w+') as f:
            for d in data:
                if d not in test:
                    f.write(d)
        names.append(name+'.test')
        with open(name+'.test', 'w+') as f:
            for d in test:
                f.write(d)
    return names
