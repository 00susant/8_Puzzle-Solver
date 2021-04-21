import pydot
from time import time

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


########################################################################################################


s = Stack()
explored = []

def dfs(initial_state):
    graph = pydot.Dot(graph_type='digraph', label="8 Puzzle State Space (DFS)", fontsize="30", color="red",
                      fontcolor="blue", style="filled", fillcolor="black")
    start_node = Puzzle(initial_state, None, None,0)
    if start_node.goal_test():
        return start_node.find_solution()
    s=Stack()
    s.push(start_node)
    explored=[]
    print("The starting node is \ndepth=%d\n" % start_node.depth)
    print(start_node.display())
    while not(s.isEmpty()):
        node=s.pop()
        print("the node selected to expand is\n")
        print("depth=%d\n" % node.depth)
        print(node.display())
        explored.append(node.state)
        graph.add_node(node.graph_node)
        if node.parent:
            graph.add_edge(pydot.Edge(node.parent.graph_node, node.graph_node,label=str(node.action)))
        if node.depth<5:
            children=node.generate_child()
            print("the children nodes of this node are\n")
            for child in children:
                if child.state not in explored :
                    print("depth=%d\n"%child.depth)
                    print(child.display())
                    if child.goal_test():
                        print("This is the goal state")
                        graph.add_node(child.graph_node)
                        graph.add_edge(pydot.Edge(child.parent.graph_node, child.graph_node, label=str(child.action)))
                        draw_legend(graph)
                        graph.write_png('solution.png')
                        return child.find_solution()
                    s.push(child)
        else:
            print("the depth has exceeded its limit, so we don't expand this node.\n")
    return

def draw_legend(graph):
    graphlegend = pydot.Cluster(graph_name="legend", label="Legend", fontsize="20", color="red",
                                fontcolor="blue", style="filled", fillcolor="white")

    legend1 = pydot.Node('Processed node', shape="plaintext")
    graphlegend.add_node(legend1)
    legend2 = pydot.Node("Depth limit reached", shape="plaintext")
    graphlegend.add_node(legend2)
    legend3 = pydot.Node('Goal Node', shape="plaintext")
    graphlegend.add_node(legend3)


    node1 = pydot.Node("1", style="filled", fillcolor="green", label="")
    graphlegend.add_node(node1)
    node2 = pydot.Node("2", style="filled", fillcolor="cyan", label="")
    graphlegend.add_node(node2)
    node3 = pydot.Node("3", style="filled", fillcolor="gold", label="")
    graphlegend.add_node(node3)


    graph.add_subgraph(graphlegend)
    graph.add_edge(pydot.Edge(legend1, legend2, style="invis"))
    graph.add_edge(pydot.Edge(legend2, legend3, style="invis"))

    graph.add_edge(pydot.Edge(node1, node2, style="invis"))
    graph.add_edge(pydot.Edge(node2, node3, style="invis"))



#############################################################################################


class Puzzle:
    # goal_state=[2,8,3,
    #             0,1,6,
    #             7,5,4]

    goal_state=[1,2,3,
                8,0,4,
                7,6,5]

    num_of_instances=0
    def __init__(self,state,parent,action,depth):
        self.parent=parent
        self.state=state
        self.action=action
        self.depth=depth
        if self.goal_test():
            color="gold"
        elif self.depth>=5:
            color="cyan"
        else:
            color="green"
        self.graph_node = pydot.Node(str(self), style="filled", fillcolor=color)
        Puzzle.num_of_instances+=1

    def display(self):
        list=self.state
        string=""
        for i in range(9):
            if (i + 1) % 3 != 0:
                if list[i]==0:
                    string += ("|   ")
                else:
                    string+=("| %d "% list[i])
            else:
                if list[i]==0:
                    string += ("|   \n")
                else:
                    string+=("| %d |\n" %list[i])
        string+="\n"
        return string

    def __str__(self):
        return self.display()

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if i == 0:  # up is disable
            legal_action.remove('UP')
        elif i == 2:  # down is disable
            legal_action.remove('DOWN')
        if j == 0:
            legal_action.remove('LEFT')
        elif j == 2:
            legal_action.remove('RIGHT')
        return legal_action

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_legal_actions(i,j)
        depth=self.depth+1

        for action in legal_actions:
            new_state = self.state.copy()
            if action is 'UP':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action is 'DOWN':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action is 'LEFT':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'RIGHT':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,depth))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution



##################################################################################################################




initial_state= [2, 8, 3,
                1, 6, 4,
                7, 0, 5]

Puzzle.num_of_instances=0
t0=time()
solution=dfs(initial_state)
t1=time()-t0
print('Solution:', solution)
print('space:',Puzzle.num_of_instances)
print('time:',t1,"seconds")
print()



