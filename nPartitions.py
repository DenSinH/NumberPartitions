import time

prevres = {}

t0 = time.time()

def NoPartitions(n, L=1):
    global prevres
    # L is the minimum value for lambda we are checking
    # we are checking in inreasing size, instead of decreasing
    if L < n:
        # coef is result
        # i is amount of lambdas with this size
        coef = 0
        i = 0
        # if L*i is greater than n, we needn't check if we can add more 
        # lambdas of this size.
        while L*i <= n:
            # if it is less, we can check for bigger lambdas
            # the "rest" is n - L*i, we need to "fill" this rest with
            # bigger lambdas
            if L*i < n:
                # try to fetch a previously gotten result to save time
                # otherwise, we get the amount of partitions with 
                # n = n-L*i, where the minimum length of lambda is L + 1
                try:
                    coef += prevres[(n - L*i, L + 1)]
                except KeyError:
                    coef += NoPartitions(n - L*i, L=L + 1)
            # if it is equal, we have reached the end for this lambda
            # and we have found one more proper partition
            elif L*i == n:
                coef += 1
                break
            # otherwise it is still the end, but we did not find a partition
            else:
                break
            
            # increment the amount of lambdas with length L for the next loop
            i += 1
            
        # store gotten result for this n and L and return it
        prevres[(n, L)] = coef
        return coef
    
    elif L == n:
        return 1
    return 0

"""Enter n and hit run!"""
n = 100

print(NoPartitions(n))
print("Computation time:", time.time() - t0)