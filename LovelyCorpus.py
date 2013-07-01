import sys
import random
from types import *

def kfold(fname, k):
    """
    Creates 'k' training files and 'k' test files.

    The file reference by 'fname' should be in the standard formatting 
    referenced in the documentation.  The names of the training and test
    files will be based on the provided 'fname'.
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
    for i in range(k):
        if i == k-1:
            test = unused
        else:
            test = []
            for j in range(foldsize):
                item = unused.pop(random.randrange(len(unused))
                test.append(item)
        name = rname + str(i)
        with open(name+'.train', 'w+') as f:
            for d in data:
                if d not in test:
                    f.write(d)
        with open(name+'.test', 'w+') as f:
            for d in test:
                f.write(d)
