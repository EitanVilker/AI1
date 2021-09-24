
from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.depth = 9999999
        self.parent = parent
        self.state = state

# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def move_animals(node, possible_new_state, search_problem, solution):
    if possible_new_state in search_problem.node_dict:
        old_node = search_problem.node_dict[possible_new_state]
        if node.depth + 1 < old_node.depth:
            old_node.depth = node.depth + 1
            old_node.parent = node
            return old_node
        return "BadPath"

    new_node = SearchNode(possible_new_state)
    new_node.depth = node.depth + 1
    new_node.parent = node
    search_problem.node_dict[possible_new_state] = new_node
    solution.nodes_visited += 1
    return new_node
    

def bfs_search(search_problem, solution=None, node=None):

    # Initialize first node
    if node == None:
        node = SearchNode(search_problem.start_state)
        node.depth = 0
        search_problem.node_dict[search_problem.start_state] = node
        solution = SearchSolution(search_problem, "BFS")
        solution.nodes_visited = 1
    
    a, b, c = search_problem.start_state
    x, y, z = node.state
    other_bank_state = (a - x, b - y, c - z)

    # Base case
    if node.state == search_problem.goal_state:
        solution.path.append(node.state)
        while node.parent != None:
            node = node.parent
            solution.path.insert(0, node.state)

        # Reset problem for next traversal
        search_problem.total_chickens = search_problem.start_state[0]
        search_problem.total_foxes = search_problem.start_state[1]
        search_problem.total_boats = search_problem.start_state[2]
        search_problem.frontier = []
        search_problem.node_dict.clear()

        return solution

    # Starting bank
    if node.state[2] > 0:

        # Move 1 chicken
        if (node.state[0] > node.state[1] or node.state[0] == 1) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 1:
            possible_new_state = (node.state[0] - 1, node.state[1], node.state[2] - 1) 
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 1 fox
        if ((other_bank_state[1] < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] - 1, node.state[2] - 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))
        
        # Move 1 fox and 1 chicken
        if node.state[0] > 0 and node.state[1] > 0 and other_bank_state[1] <= other_bank_state[0]:
            possible_new_state = (node.state[0] - 1, node.state[1] - 1, node.state[2] - 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 2 chickens
        if (node.state[0] - 1 > node.state[1] or node.state[0] == 2) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 2:
            possible_new_state = (node.state[0] - 2, node.state[1], node.state[2] - 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 2 foxes
        if ((other_bank_state[1] + 1 < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] - 2, node.state[2] - 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))
        

    # Other bank
    if other_bank_state[2] > 0:

        # Move 1 chicken
        if (other_bank_state[0] == 1 or other_bank_state[0] > other_bank_state[1]) and other_bank_state[0] > 0 and node.state[1] <= node.state[0] + 1:
            possible_new_state = (node.state[0] + 1, node.state[1], node.state[2] + 1) 
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 1 fox
        if (node.state[1] < node.state[0] or node.state[0] == 0) and other_bank_state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] + 1, node.state[2] + 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))
        
        # Move 1 fox and 1 chicken
        if other_bank_state[0] > 0 and other_bank_state[1] > 0 and node.state[1] <= node.state[0]:
            possible_new_state = (node.state[0] + 1, node.state[1] + 1, node.state[2] + 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 2 chickens
        if (other_bank_state[0] - 1 > other_bank_state[1] or other_bank_state[0] == 2) and other_bank_state[0] > 1 and node.state[1] <= node.state[0] + 2:
            possible_new_state = (node.state[0] + 2, node.state[1], node.state[2] + 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

        # Move 2 foxes
        if ((node.state[1] + 1 < node.state[0]) or (node.state[0] == 0)) and other_bank_state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] + 2, node.state[2] + 1)
            search_problem.frontier.append(move_animals(node, possible_new_state, search_problem, solution))

    # Check that next node in frontier is valid and recursively apply bfs
    if len(search_problem.frontier) > 0:
        next_node = search_problem.frontier.pop(0)
        while next_node == "BadPath" and len(search_problem.frontier) > 0:
            next_node = search_problem.frontier.pop(0)
        solution.nodes_visited += 1
        if next_node != "BadPath":
            return bfs_search(search_problem, solution, node=next_node)
    return None

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        node.depth = 0
        search_problem.node_dict[search_problem.start_state] = node
        solution = SearchSolution(search_problem, "DFS")
        solution.nodes_visited = 1

    new_frontier = []
    a, b, c = search_problem.start_state
    x, y, z = node.state
    other_bank_state = (a - x, b - y, c - z)

    # Base case
    if node.state == search_problem.goal_state:
        solution.path.append(node.state)
        while node.parent != None:
            node = node.parent
            solution.path.insert(0, node.state)

        # Reset the problem so other graph traversals can be done
        search_problem.total_chickens = search_problem.start_state[0]
        search_problem.total_foxes = search_problem.start_state[1]
        search_problem.total_boats = search_problem.start_state[2]
        search_problem.frontier = []
        search_problem.node_dict.clear()

        return solution

    # Starting bank
    if node.state[2] > 0:

        # Move 1 chicken
        if (node.state[0] > node.state[1] or node.state[0] == 1) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 1:
            possible_new_state = (node.state[0] - 1, node.state[1], node.state[2] - 1) 
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox
        if ((other_bank_state[1] < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] - 1, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox and 1 chicken
        if node.state[0] > 0 and node.state[1] > 0 and other_bank_state[1] <= other_bank_state[0]:
            possible_new_state = (node.state[0] - 1, node.state[1] - 1, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 chickens
        if (node.state[0] - 1 > node.state[1] or node.state[0] == 2) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 2:
            possible_new_state = (node.state[0] - 2, node.state[1], node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 foxes
        if ((other_bank_state[1] + 1 < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] - 2, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

    # Other bank
    if other_bank_state[2] > 0:

        # Move 1 chicken
        if (other_bank_state[0] == 1 or other_bank_state[0] > other_bank_state[1]) and other_bank_state[0] > 0 and node.state[1] <= node.state[0] + 1:
            possible_new_state = (node.state[0] + 1, node.state[1], node.state[2] + 1) 
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)
        
        # Move 1 fox
        if (node.state[1] < node.state[0] or node.state[0] == 0) and other_bank_state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] + 1, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox and 1 chicken
        if other_bank_state[0] > 0 and other_bank_state[1] > 0 and node.state[1] <= node.state[0]:
            possible_new_state = (node.state[0] + 1, node.state[1] + 1, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 chickens
        if (other_bank_state[0] - 1 > other_bank_state[1] or other_bank_state[0] == 2) and other_bank_state[0] > 1 and node.state[1] <= node.state[0] + 2:
            possible_new_state = (node.state[0] + 2, node.state[1], node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 foxes
        if ((node.state[1] + 1 < node.state[0]) or (node.state[0] == 0)) and other_bank_state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] + 2, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node) 

    # Update frontier
    search_problem.frontier = new_frontier + search_problem.frontier    

    # Get next node from frontier with depth less than limit and recursively apply dfs
    if len(search_problem.frontier) == 0:
        return None
    next_node = search_problem.frontier.pop(0)
    while (next_node == "BadPath" or next_node.depth > depth_limit) and len(search_problem.frontier) > 0:
        next_node = search_problem.frontier.pop(0)
    solution.nodes_visited += 1
    return dfs_search(search_problem, solution=solution, node=next_node)


def ids_search(search_problem, depth_limit=80, node=None, solution=None, current_depth=0):

    if solution == None:
        solution = SearchSolution(search_problem, "IDS")
    solution.nodes_visited += 1
    
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        node.depth = 0
        search_problem.node_dict[search_problem.start_state] = node

    new_frontier = []
    a, b, c = search_problem.start_state
    x, y, z = node.state
    other_bank_state = (a - x, b - y, c - z)

    # Base case
    if node.state == search_problem.goal_state:
        solution.path.append(node.state)
        while node.parent != None:
            node = node.parent
            solution.path.insert(0, node.state)

        # Reset the problem so other graph traversals can be done
        search_problem.total_chickens = search_problem.start_state[0]
        search_problem.total_foxes = search_problem.start_state[1]
        search_problem.total_boats = search_problem.start_state[2]
        search_problem.frontier = []
        search_problem.node_dict.clear()

        return solution

    # Starting bank
    if node.state[2] > 0:

        # Move 1 chicken
        if (node.state[0] > node.state[1] or node.state[0] == 1) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 1:
            possible_new_state = (node.state[0] - 1, node.state[1], node.state[2] - 1) 
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox
        if ((other_bank_state[1] < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] - 1, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox and 1 chicken
        if node.state[0] > 0 and node.state[1] > 0 and other_bank_state[1] <= other_bank_state[0]:
            possible_new_state = (node.state[0] - 1, node.state[1] - 1, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 chickens
        if (node.state[0] - 1 > node.state[1] or node.state[0] == 2) and node.state[0] > 0 and other_bank_state[1] <= other_bank_state[0] + 2:
            possible_new_state = (node.state[0] - 2, node.state[1], node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 foxes
        if ((other_bank_state[1] + 1 < other_bank_state[0]) or (other_bank_state[0] == 0)) and node.state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] - 2, node.state[2] - 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)
    
    # Other bank
    if other_bank_state[2] > 0:
        # Move 1 chicken
        if (other_bank_state[0] == 1 or other_bank_state[0] > other_bank_state[1]) and other_bank_state[0] > 0 and node.state[1] <= node.state[0] + 1:
            possible_new_state = (node.state[0] + 1, node.state[1], node.state[2] + 1) 
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)
        
        # Move 1 fox
        if (node.state[1] < node.state[0] or node.state[0] == 0) and other_bank_state[1] > 0:
            possible_new_state = (node.state[0], node.state[1] + 1, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 1 fox and 1 chicken
        if other_bank_state[0] > 0 and other_bank_state[1] > 0 and node.state[1] <= node.state[0]:
            possible_new_state = (node.state[0] + 1, node.state[1] + 1, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)

        # Move 2 chickens
        if (other_bank_state[0] - 1 > other_bank_state[1] or other_bank_state[0] == 2) and other_bank_state[0] > 1 and node.state[1] <= node.state[0] + 2:
            possible_new_state = (node.state[0] + 2, node.state[1], node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node)
                
        # Move 2 foxes
        if ((node.state[1] + 1 < node.state[0]) or (node.state[0] == 0)) and other_bank_state[1] > 1:
            possible_new_state = (node.state[0], node.state[1] + 2, node.state[2] + 1)
            new_node = move_animals(node, possible_new_state, search_problem, solution)
            if new_node != "BadPath":
                new_frontier.append(new_node) 
    
    # Update frontier
    search_problem.frontier = new_frontier + search_problem.frontier    

    # If frontier is empty and depth exceeded, stop search. If depth limit not yet reached, do ids with increased depth
    if len(search_problem.frontier) == 0:
        if current_depth >= depth_limit:
            return None
        current_depth += 1
        
        # Reset search problem
        search_problem.total_chickens = search_problem.start_state[0]
        search_problem.total_foxes = search_problem.start_state[1]
        search_problem.total_boats = search_problem.start_state[2]
        search_problem.frontier = []
        search_problem.node_dict.clear()
        return ids_search(search_problem, current_depth=current_depth, solution=solution)
    
    # Get next valid node from frontier with depth less than limit
    next_node = search_problem.frontier.pop(0)
    while (next_node == "BadPath" or next_node.depth > depth_limit or next_node.depth >= current_depth) and len(search_problem.frontier) > 0:
        next_node = search_problem.frontier.pop(0)
    
    # solution.nodes_visited += 1

    if (next_node == "BadPath" or next_node.depth > depth_limit or next_node.depth >= current_depth) and len(search_problem.frontier) == 0:
        current_depth += 1
        
        # Reset search problem
        search_problem.total_chickens = search_problem.start_state[0]
        search_problem.total_foxes = search_problem.start_state[1]
        search_problem.total_boats = search_problem.start_state[2]
        search_problem.frontier = []
        search_problem.node_dict.clear()
        return ids_search(search_problem, current_depth=current_depth, solution=solution)

    return ids_search(search_problem, solution=solution, node=next_node, current_depth=current_depth)