class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_chickens = start_state[0]
        self.total_foxes = start_state[1]
        self.total_boats = start_state[2]
        self.frontier = []
        self.node_dict = {}

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list
        if state in node_dict:
            node = node_dict[state]
            successors = []
            successors.insert(0, node.state)
            while node.parent != None:
                node = node.parent
                successors.insert(0, node.state)
            return successors
        return None

    # I also had a goal test method. You should write one.

    def __str__(self):
        string =  "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    # print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
