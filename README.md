# NumberPartitions
A few scripts I made a while ago for some school project

Basically what it does is it calculates the number of partitions for a given number. 

### Partitions

A partition of a number n is a tuple of strictly positive integers that add up to n. This tuple must be ordered from largest to smallest. So for example (4, 3, 1, 1) is a partition of 9, but (4, 1, 3, 1) is not. There are different ways to calculate the amount of partitions. The script nPartitions.py does this in a pretty quick way. You can also do it in an exact way, using a formula that you can derive from a product of polynomials of infinite degree. exact.py does it this way using SciPy, and is considerably slower. 

### Flat/Solid partitions

Besides normal partitions, you can also define flat or solid partitions. This is basically a 2 or 3D extension of normal partitions. Instead of looking at a tuple of numbers, you would look at a matrix, so for example

|   |   |   |
|---|---|---|
| 3 | 1 | 1 |
| 1 | 1 |   |
| 1 | 1 |   |

(I don't know how to make proper tables, leave me be.) Is an example of a flat partition of 9. In this case, the numbers must always be non-increasing whenever you go right or down. the script flatPartitions.py calculates the amount of these exist for any given number. For this I used the normal partitions, so instead of just counting them (which is what I did before), I had to actually find the representations. Solid partitions are defined in a similar manner, but then in 3D. I basically used the same approach for these as I did for the flat partitions. You can expand this idea to 4, 5 or n dimensions, and the script I wrote can easily be expanded as well. (If I remember correctly, you would only have to add another loop, I never got around to generalizing it).

I wrote this script for a professor who does not have much coding experience, so it may be a bit overcommented.
