<h1>
    
    CS76
    21F
    PA1
    Eitan Vilker
    
</h1>

## Description

For my breadth-first search, I begin by initalizing an empty node. Then, I check the base case, clearing the problem and returning the solution in the case that the goal has been reached. Next, I examine all possible states, pushing the legal ones to the frontier. This is separated by which bank the boat is on. Finally, I check to see if there is a valid node to visit, and if so, conduct another search on that node, removing it from the frontier. If not, the search terminates and returns None. In order to test my breadth-first search algorithm, I set the goal state to (1, 1, 0), the last state I put into my graph. My program found the exact same path as I did to get to (1, 1, 0), so it seems very likely correct.

Here is the output my algorithm produces for (3, 3, 1):

    Chickens and foxes problem: (3, 3, 1)
    attempted with search method BFS
    number of nodes visited: 29
    solution length: 12
    path: [(3, 3, 1), (2, 2, 0), (3, 2, 1), (3, 0, 0), (3, 1, 1), (1, 1, 0), (2, 2, 1), (0, 2, 0), (0, 3, 1), (0, 1, 0), (1, 1, 1), (0, 0, 0)]

My depth-first search functions similarly to my breadth-first search until it comes time to add nodes to the frontier. Instead, it creates a temporary frontier, and after adding all possible next steps to it, puts the temporary frontier at the front of the actual frontier. In this way, individual paths are examined first instead of expanding outward slowly like bfs. Like breadth-first search, I then check to see if there is a valid node to visit, and if so, conduct another search on that node, removing it from the frontier. If not, the search terminates and returns None. 

Here is the output my algorithm produces for (3, 3, 1):

    Chickens and foxes problem: (3, 3, 1)
    attempted with search method DFS
    number of nodes visited: 27
    solution length: 12
    path: [(3, 3, 1), (2, 2, 0), (3, 2, 1), (3, 0, 0), (3, 1, 1), (1, 1, 0), (2, 2, 1), (0, 2, 0), (0, 3, 1), (0, 1, 0), (1, 1, 1), (0, 0, 0)]

For ids, I decided not to simply run dfs repeatedly in a loop as suggested. Instead, I thought I could do it without a loop altogether. I accomplished this by preventing nodes from being followed if they were over over the recursion limit, and if no eligible nodes existed, resetting the problem and calling ids with a higher current depth, all recursively. I would be curious to see if this approach had any effect on the runtime relative to others in the class.

Here is the output my algorithm produces for (3, 3, 1):

    Chickens and foxes problem: (3, 3, 1)
    attempted with search method IDS
    number of nodes visited: 208
    solution length: 12
    path: [(3, 3, 1), (2, 2, 0), (3, 2, 1), (3, 0, 0), (3, 1, 1), (1, 1, 0), (2, 2, 1), (0, 2, 0), (0, 3, 1), (0, 1, 0), (1, 1, 1), (0, 0, 0)]

As expected, ids looks at many more nodes than either of the other two algorithms, accounting for the greater runtime. It seems clear that bfs is the best for this kind of problem, with limited legal actions and a highly connected graph. If the graph was less connected, and there were a bunch of long, unbranching paths, then I would imagine ids would have better performance than breadth-first search.

## Evaluation
My program succeeded at producing ideal solutions for bfs and ids in the tests I ran. I think my path-checking was flawed and too close to memoizing, so my memory storage may not have been optimal for dfs, although its efficiency and accuracy were good. Otherwise, however, I believe my program performed as desired, with even a little bit of extra capability added for having multiple boats. Using the Python time library, I computed the time for each method as shown below.

| Method      | Problem     | Time (s)   |
| ----------- | ----------- | -----------
| BFS         | (3, 3, 1)   | 0.00341    |
| DFS         | (3, 3, 1)   | 0.00229    |
| IDS         | (3, 3, 1)   | 0.00510    |
| BFS         | (5, 5, 1)   | 0.00114    |
| DFS         | (5, 5, 1)   | 0.00101    |
| IDS         | (5, 5, 1)   | 0.01814    |
| BFS         | (5, 4, 1)   | 0.00534    |
| DFS         | (5, 4, 1)   | 0.00668    |
| IDS         | (5, 4, 1)   | 0.00827    |

Depth-first search was generally the fastest, as we would expect. It did struggle with the last one a bit, presumably because there were many nodes and relatively short paths. Interestingly, I got better performance for bfs and dfs with (5, 5, 1), the case that no path existed. These methods must have been able to quickly evaluate that no paths existed. However, ids attempted the same paths over and over again, going all the way to the depth limit, because it could not terminate earlier unless a goal had been reached. With more time, I would have attempted to design the algorithm such that it would track the furthest node it had reached, and if no node was found past that point, terminate early.

## Discussion

### Implement the Model: States and Actions
Without considering the legality of states, we can assume that the maximum number of states is (x+1)(y+1)(z+1), where x, y, and z are the first, second, and third starting valus of the tuple, respectively. This is because we can potentially have any number of chickens, foxes, and boats between 0 and the starting values. As an example, for the muber of chickens, we can have 0, 1, 2, or 3 on the starting bank at any given point, each of which is idependent from the number of foxes or boats if we disregard legality. Therefore, for the problem (3, 3, 1) we can compute (3+1)(3+1)(1+1), which evaluates to 32 possible states.

For the below graph, legal states are bolded and have the letter "L" at the end, while illegal states are not bolded and have the letter "I" at the end. The initial state is 331L, as shown in the bottom right. All edges are bidirectional.

![graph (1)](https://user-images.githubusercontent.com/38114628/134617244-f67bf32e-0b35-432e-95c8-4f19d20d2a45.png)

### Implement Path-Checking Depth-First Search

Below is a graph that produces a significantly worse run-time with depth-first search than with breadth-first search. Assuming that A is the start and C is the goal , and that nodes are added to the frontier in alphabetical order, breadth-first search would look at node A, then B, than C, and finish there. However, depth-first search would look at every single node along the path starting from B before it looked at C. We can conclude from this that depth-first search is worse when there are many nodes but only a small distance to the goal. 

![graph (2)](https://user-images.githubusercontent.com/38114628/134617842-90f812e3-a6f7-4819-b6f1-e6c930dde892.png)

### Iterative Deepening Search


