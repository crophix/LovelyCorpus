####################################################
# Copyright (c) 2013 Daniel Leblanc
#
# This program is released under the 'MIT License'. Please
# see the file COPYING in this distribution for license terms.
####################################################

"""
Lovely Coorpus is a corpus management toolkit designed to make sanitizing
data sets easier.
"""

import sys
import random
import math
from types import *

FIRST = 0
LAST = -1

def attributeCount(data):
    """
    Verify that all elements in the data have the same number of attributes.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    data = _checkData(data)
    l = len(data[0])
    for d in data:
        if len(d) != l:
            return False
        for a in d:
            if a == '':
                return False
    return True

def removeOutliers(data, amount, clposition=LAST, newfname=None):
    """
    Remove a given amount of data outliers.

    The amount provided can either be an integer value or a decimal value.
    If it is an integer that number of outliers are removed.  If it is a 
    decimal that percentage of outliers are removed.  Outliers are 
    determined using their Euclidean distance from the mean for their class.
        
    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    if type(amount) is IntType:
        isint = True
    else:
        assert type(amount) is FloatType
        isint = False
    if not newfname:
        assert type(data) is StringType
        newfname = data
    data = _checkData(data)
    avg = _getaverage(data, clposition)
    dist = []
    for d in data:
        cl = d.pop(clposition)
        total = 0
        for i in len(d):
            total += (avg[cl][i] - float(d[i]))**2
        dist.append(total**0.5)
    if not isint:
        amount = int(len(data) * amount + 0.9)
    for i in range(amount):
        x = dist.index(max(dist))
        dist.pop(x)
        data.pop(x)
    if not newfname:
        newfname = fname
    with open(newfname, 'w+') as f:
        for d in data:
            f.write(','.join(str(x) for x in d) + '\n')
    return

def _getaverage(data, clposition):
    total = {}
    count = {}
    for d in data:
        cl = d.pop(clposition)
        if total.has_key(cl):
            count[cl] += 1.0
            for i in len(d):
                total[cl][i] += float(d[i])
        else:
            count[cl] = 1.0
            total[cl] = d
    avg = {}
    for k in total.keys():
        avg[k] = total[k] / count[k]
    return avg
    
def checkDuplicates(data, remove=False, fname=None):
    """
    Check the data for an duplicate entries.

    If the remove flag is set, duplicates are removed and the data is
    written to the file name provided.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    data = _checkData(data)
    if remove:
        assert type(fname) is StringType
    for i in range(len(data)):
        d = data.pop(0)
        if d in data:
            if not remove:
                return False
        else:
            data.append(d)
    if remove:
        with open(fname, 'w+') as f:
            for d in data:
                f.write(','.join(str(x) for x in d) + '\n')
    return True

def setIntRange(data, mn, mx, clposition=LAST, attr=[], newfname=None):
    """
    Change attributes so that they fall within the given range.

    All attributes are changed to be integers that fall within the range. 
    The range is defined as inclusive of the min and max values provided.
    i.e. [mn, mx]. The index of the classifier for each entry is stored
    in the clposition variable.  If only certain attributes should be 
    changed a list of indices can be included in the attr variable. The
    default behavior is to overwrite the existing file, but a new file 
    name can be included.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    assert type(mn) is IntType
    assert type(mx) is IntType
    assert type(clposition) is IntType
    assert type(attr) is ListType
    assert mn < mx
    if newfname:
        assert type(newfname) is StringType
    elif type(data) is StringType:
        newfname = data
    else:
        sys.exit("A filename nust be provided for setIntRange")
    data = _checkData(data)
    if attr == []:
        attr = range(len(data[0]))
        attr.pop(clposition)
    curMax = mx
    curMin = mn
    for i in range(len(data)):
        for a in attr:
            curMax = max(float(data[i][a]), curMax)
            curMin = min(float(data[i][a]), curMin)
    div = mx - mn + 1.0
    scale = div/(curMax - curMin + 1.0)
    for i in range(len(data)):
        for a in attr:
            data[i][a] = int(mn + (int(data[i][a])*scale))
    with open(newfname, 'w+') as f:
        for d in data:
            f.write(','.join(str(x) for x in d) + '\n')
    return

def kfold(fname, k):
    """
    Creates 'k' training files and 'k' test files.

    The file referenced by 'fname' can be relative or absolute path name.  
    The names of the training and test files will be based on the provided 
    'fname'.  Any suffix on the provided file name will be discarded and 
    replaced with either "train" or "test".

    Example: 
        k = 2
        fname = "data.txt"
        output = ["data0.train", "data0.test", "data1.train", "data1.test"]

    A list of filenames will be returned.
    """
    assert type(k) is IntType
    assert type(fname) is StringType
    assert k > 1
    data = []
    try:
        with open(fname) as f:
            for l in f:
                data.append(l)
    except IOError:
        print "Invalid Filename"
        return
    rname = fname.rsplit('.', 1)[0]
    extr = 0
    if len(data) % k != 0:
        extr = 1
    foldsize = len(data) / k + extr
    unused = list(data)
    names = []
    for i in range(k):
        if i == k-1:
            test = unused
        else:
            test = []
            for j in range(foldsize):
                item = unused.pop(random.randrange(len(unused)))
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

def entropyGain(data, clposition=LAST):
    """
    Computes the entropy gain of each attributes and returns a list 
    of those values.

    The list of values match the positions of the attributes in the file.
    The entropy gain is weighted by the number of different values that are
    possible for the attribute.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    assert type(clposition) is IntType
    data = _checkData(data)
    egains = []
    for a in range(len(data[0])):
        egains.append(egain(data, a, clposition))
    egains.pop(clposition)
    return egains

def egain(data, attr, clposition):
    """
    Compute the entropy gain of a given attribute.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    assert type(attr) is IntType
    assert type(clposition) is IntType
    data = _checkData(data)
    freq = {}
    subentropy = 0.0
    for d in data:
        if freq.has_key(d[attr]):
            freq[d[attr]] += 1.0
        else:
            freq[d[attr]] = 1.0
    for a in freq.keys():
        prob = freq[a] / sum(freq.values())
        data_subset = [d for d in data if d[attr] == a]
        subentropy += prob * _entropy(data_subset, clposition)
    return _entropy(data, clposition) - subentropy

def _entropy(data, clposition):
    entropy = 0.0
    freq = {}
    for d in data:
        if freq.has_key(d[clposition]):
            freq[d[clposition]] += 1.0
        else:
            freq[d[clposition]] = 1.0
    for f in freq.values():
        entropy += -(f/len(data) * math.log(f/len(data), 2))
    return entropy

def checkRange(data, minval, maxval, checklist=[], clposition=LAST, remove=False, truncate=False):
    """
    Verify that the attributes are with the provided range.

    If no checklist is provided all attributes except the class identifier
    are checked against the provided range.  If the remove flag is set, any line 
    containing a value outside the range are removed.  If the truncate flag
    is set the values will be truncated to fall within the provided range.  If 
    the remove or truncate flag are not set, a list of the line numbers that contain
    out of bounds values is returned.  Non numerical attributes that are included 
    in the checklist are ignored.

    The 'data' variable can be a file name (example.txt), a list of comma 
    separated strings (["1,2,3", "4,5,6", ...]), or a list of already separated 
    values ([[1, 2, 3], [4, 5, 6], ...]).
    """
    assert type(checklist) is ListType
    assert type(minval) is IntType
    assert type(maxval) is IntType
    assert minval < maxval
    assert type(clposition) is IntType
    assert type(remove) is BooleanType
    assert type(truncate) is BooleanType
    if remove or truncate:
        assert type(data) is StringType
        fname = data
    data = _checkData(data)
    if checklist == []:
        checklist=range(len(data[0]))
        checklist.pop(clposition)
    linenums = []
    for i in range(len(data)):
        for a in checklist:
            try:
                if float(data[i][a]) > maxval:
                    data[i][a] = str(maxval)
                    linenums.append(i)
                elif float(data[i][a]) < minval:
                    data[i][a] = str(minval)
                    linenums.append(i)
            except ValueError:
                pass
    if remove:
        #Pop the offending line numbers in reverse order
        linenums = list(set(linenums))
        linenums.sort()
        linenums.reverse()
        for l in linenums:
            data.pop(l)
    if remove or truncate:
        with open(fname) as f:
            for d in data:
                f.write(','.join(d) + '\n')
    else:
        return linenums

def _checkData(data):
    if type(data) is StringType:
        try:
            with open(data) as f:
                data = []
                for l in f:
                    data.append(l)
        except IOError:
            print "Invalid Filename"
            sys.exit(0)
    if type(data) is ListType:
        if type(data[0]) is not ListType:
            assert type(data[0]) is StringType
            data = [d.split(',') for d in data]
    return data
