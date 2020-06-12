import time
import numpy as np
import copy

t0 = time.time()

showres = {}

"""
Function to find the actual partitions
!!! TAKES MORE MEMORY, DO NOT USE FOR HIGH n !!!
"""

def ShowPartitions(n, L=1):
    global showres
    # L is the lambda we are checking
    # we are checking in inreasing size, instead of decreasing
    parts = []
    if L < n:
        # i is amount of lambdas with this size
        i = 0
        # if L*i is greater than n, we needn't check if we can add more 
        # lambdas of this length.
        while L*i <= n:
            # if it is less, we can check for longer lambdas
            # the "rest" is n - L*i, we need to "fill" this rest with
            # longer lambdas
            if L*i < n:
                # try to fetch a previously gotten result to save time
                # otherwise, we get the amount of partitions with 
                # n = n-L*i, where the minimum length of lambda is L + 1
                try:
                    NextRes = showres[(n - L*i, L + 1)]
                except KeyError:
                    NextRes = ShowPartitions(n - L*i, L=L + 1)
                
                for res in NextRes:
                    parts.append([L]*i + res)
            # if it is equal, we have reached the end for this lambda
            # and we have found one more proper partition
            elif L*i == n:
                parts.append([L]*i)
                break
            # otherwise it is still the end, but we did not find a partition
            else:
                break
            
            # increment the amount of lambdas with length L for the next loop
            i += 1
            
        # store gotten result for this n and L and return it
        showres[(n, L)] = parts
        return parts
    
    elif L == n:
        return [[L]]
    return []


"""
Function that finds all proper "box configurations" for a given partition
of n
"""

def flatpart(part, startgrid=None, originlength=0):
    # originlength is the length of the original partition
    originlength = max(originlength, len(part))
    
    # if no startgrid is passed, create a starting grid
    # this grid consists of zeros, with the first element of the partition
    # in the top left corner (this must be)
    if startgrid is None:
        startgrid = np.zeros((originlength + 1, originlength + 1))
        # + 1 is to have an extra zero below and left to avoid using a
        # try/except statement
        startgrid[0, 0] = part[0]
        
        # if the partition is made up of one element and no starting grid was
        # passed, then the only possible configuration is the created
        # startgrid
        if len(part) == 1:
            return [startgrid]
        
        # if this was not the case, we have "used up" the first element,
        # so we only have to look at the rest (which is at least one element)
        part = part[1:]
        
    # list for the proper flats
    flats = []
    # loop over all i and j
    for i in range(originlength):
        for j in range(originlength):
            # if the space is available (equal to 0), proceed
            if startgrid[i, j] == 0:
                # check if square above and left are greater than the 
                # element we are trying to put there (if existent)
                if i == 0 or startgrid[i - 1, j] >= part[0]:
                    if j == 0 or startgrid[i, j - 1] >= part[0]:
                        # the next configuration to start flatting the 
                        # rest of the partition in is our startgrid
                        # with the first element of part (2nd of the partition)
                        # in the selected spot
                        nextgrid = copy.copy(startgrid)
                        nextgrid[i, j] = part[0]
                        
                        # if there was only one element left in the partition,
                        # we have found one proper flat, so we compare them to
                        # all the ones previously found and append it 
                        # accordingly
                        if len(part) == 1:
                            for flat in flats:
                                if (nextgrid == flat).all():
                                    break
                            else:
                                flats += [nextgrid]
                        
                        # otherwise we look at the flats of the rest of our
                        # partition, starting with the nextgrid we created
                        else:
                            NextFlats = flatpart(part[1:], startgrid=nextgrid,
                                               originlength=originlength)
                            # again, compare them all to previous results,
                            # and append them accordingly
                            for flat in NextFlats:
                                for compareflat in flats:
                                    if (flat == compareflat).all():
                                        break
                                else:
                                    flats += [flat]
                
                # if the element left from us is 0, we have no need to check
                # further to the right
                elif j > 0 and startgrid[i, j - 1] == 0:
                    break
            
            # if the element above us is 0, we have no need to check further
            # down
            elif i > 0 and startgrid[i - 1, j] == 0:
                break
                
    # return all proper flats
    return flats


"""
Function that counts all different configurations for all partitions of n
"""
 
def p2(n, startgrid=0, show=False):
    # list of flats, and list of partitions of n
    flats = []
    nParts = ShowPartitions(n)
    for p in nParts:
        # invert the partition so it is in decreasing order
        part = p[::-1]
        
        # loop over all flat partitions and append them accordingly
        for flat in flatpart(part):
            for compareflat in flats:
                if flat.size == compareflat.size and \
                 (flat == compareflat).all():
                    break
            else:
                flats += [flat]
                
    if show:
        for flat in flats:
            print(flat)
            
    return len(flats)

""" 
Enter n and hit run!
"""
n = 5
print(p2(n, show=True))
print("Computation time:", time.time() - t0)