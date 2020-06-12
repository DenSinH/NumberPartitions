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

def solidpart(part, startspace=None, originlength=0):
    # originlength is the length of the original partition
    originlength = max(originlength, len(part))
    
    # if no startspace is passed, create a starting space
    # this space consists of zeros, with the first element of the partition
    # in the top left corner (this must be)
    if startspace is None:
        startspace = np.zeros((originlength + 1, originlength + 1, originlength + 1))
        # + 1 is to have an extra zero below and left to avoid using a
        # try/except statement
        startspace[0, 0, 0] = part[0]
        
        # if the partition is made up of one element and no starting space was
        # passed, then the only possible configuration is the created
        # startspace
        if len(part) == 1:
            return [startspace]
        
        # if this was not the case, we have "used up" the first element,
        # so we only have to look at the rest (which is at least one element)
        part = part[1:]
        
    # list for the proper solids
    solids = []
    # loop over all i and j
    for i in range(originlength):
        for j in range(originlength):
            for k in range(originlength):
                # if the space is available (equal to 0), proceed
                if startspace[i, j, k] == 0:
                    # check if square above and left are greater than the 
                    # element we are trying to put there (if existent)
                    if i == 0 or startspace[i - 1, j, k] >= part[0]:
                        if j == 0 or startspace[i, j - 1, k] >= part[0]:
                            if k == 0 or startspace[i, j, k - 1] >= part[0]:
                                # the next configuration to start solidting the 
                                # rest of the partition in is our startspace
                                # with the first element of part (2nd of the partition)
                                # in the selected spot
                                nextspace = copy.copy(startspace)
                                nextspace[i, j, k] = part[0]
                                
                                # if there was only one element left in the partition,
                                # we have found one proper solid, so we compare them to
                                # all the ones previously found and append it 
                                # accordingly
                                if len(part) == 1:
                                    for solid in solids:
                                        if (nextspace == solid).all():
                                            break
                                    else:
                                        solids += [nextspace]
                                
                                # otherwise we look at the solids of the rest of our
                                # partition, starting with the nextspace we created
                                else:
                                    NextSolids = solidpart(part[1:], startspace=nextspace,
                                                       originlength=originlength)
                                    # again, compare them all to previous results,
                                    # and append them accordingly
                                    for solid in NextSolids:
                                        for comparesolid in solids:
                                            if (solid == comparesolid).all():
                                                break
                                        else:
                                            solids += [solid]
                         # if the element left from us is 0, we have no need to check
                        # further to the right
                        elif k > 0 and startspace[i, j, k - 1] == 0:
                            break
                    
                    # if the element left from us is 0, we have no need to check
                    # further to the right
                    elif j > 0 and startspace[i, j - 1, k] == 0:
                        break
                
                # if the element above us is 0, we have no need to check further
                # down
                elif i > 0 and startspace[i - 1, j, k] == 0:
                    break
                
    # return all proper solids
    return solids


"""
Function that counts all different configurations for all partitions of n
"""
 
def p3(n, startspace=0, show=False):
    # list of solids, and list of partitions of n
    solids = []
    nParts = ShowPartitions(n)
    for p in nParts:
        # invert he partition so it is in decreasing order
        part = p[::-1]
        
        # loop over all solid partitions and append them accordingly
        for solid in solidpart(part):
            for comparesolid in solids:
                if solid.size == comparesolid.size and \
                 (solid == comparesolid).all():
                    break
            else:
                solids += [solid]
                
    if show:
        for solid in solids:
            print(solid)
            
    return len(solids)

""" 
Enter n and hit run!
"""
n = 8
print(p3(n, show=False))
print("Computation time:", time.time() - t0)