# PA1

### Implement the Model: States and Actions
Without considering the legality of states, we can assume that the maximum number of states is (x+1)(y+1)(z+1), where x, y, and z are the first, second, and third starting valus of the tuple, respectively. This is because we can potentially have any number of chickens, foxes, and boats between 0 and the starting values. As an example, for the muber of chickens, we can have 0, 1, 2, or 3 on the starting bank at any given point, each of which is idependent from the number of foxes or boats if we disregard legality. Therefore, for the problem (3, 3, 1) we can compute (3+1)(3+1)(1+1), which evaluates to 32 possible states.


### Implement Breadth-First Search
