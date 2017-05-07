import sys
from Queue import *

class Node(object):
    def __init__(self, dataset, value):
        self.dataset = dataset
        self.value = value
        self.children = []
        
    def __repr__(self):
        return "Node: [%s, %s]" % (self.value, self.dataset)
    
    def addChild(self, node):
        self.children.append(node) 
    
    def getChildren(self):
        return self.children         
    
    def getRevChildren(self):
        children = self.children[:]
        children.reverse()
        return children         

def println(text):
    sys.stdout.write(text + "\n")

'''
Creates an unordered tree with N number of children on each node from a date:value dict
@param numOfChildren - number of children per node 
@param dateValues - list of date:value dictionaries to be added to the tree
@return rootNode - root node of the created tree
'''
def createTree(numOfChildren, dateValues):
    dateValuesList = dateValues.keys()
    lengthDateValues = len(dateValuesList)
    rootNode = Node(dateValuesList[0], dateValues.get(dateValuesList[0]))
    currParentNodes = Queue()
    currParentNodes.put(rootNode)
    index = 1

    while index < lengthDateValues:
        currParentNodesSize = currParentNodes.qsize()
        for parentIndex in range(0,currParentNodesSize):
            currParentNode = currParentNodes.get()
            for childIndex in range(0, numOfChildren):
                if (index == lengthDateValues):
                    break
                childNode = Node(dateValuesList[index], dateValues.get(dateValuesList[index]))
                currParentNode.addChild(childNode)
                currParentNodes.put(childNode)
                index +=1
    return rootNode


'''
Prints out all nodes and their children
@param rootNode - root node of the tree
'''
def printAllTreeNodes(rootNode):
    currParentNodes = Queue()
    currParentNodes.put(rootNode)
    lengthCurrParentNodes = currParentNodes.qsize()
    count = 0

    while currParentNodes.qsize() > 0:
        currNode = currParentNodes.get()
        print("Current node %d value: %s dataset: %s children: %s" % (count, currNode.value, currNode.dataset, currNode.children))
        lengthOfChildren = len(currNode.children)
        if(lengthOfChildren > 0):
            for childIndex in range(0,lengthOfChildren):
                currParentNodes.put(currNode.children[childIndex])
        count +=1


'''
Gets the count of all nodes within a tree
@param rootNode - root node of the tree
@return count - count of all nodes of the tree
'''
def countOfAllTreeNodes(rootNode):
    currParentNodes = Queue()
    currParentNodes.put(rootNode)
    lengthCurrParentNodes = currParentNodes.qsize()
    count = 0

    while currParentNodes.qsize() > 0:
        currNode = currParentNodes.get()
        lengthOfChildren = len(currNode.children)
        if(lengthOfChildren > 0):
            for childIndex in range(0,lengthOfChildren):
                currParentNodes.put(currNode.children[childIndex])
        count +=1
    return count

'''
Searches a tree for a value using breadth first search. if no node has the value we are looking for,
then the closest matched node will get returned.
@param rootNode - root node of the tree
@return foundNode - node that most closely matches the value we are looking for
'''
def breadthFirstSearch(rootNode, value):
    currParentNodes = Queue()
    currParentNodes.put(rootNode)
    lengthCurrParentNodes = currParentNodes.qsize()
    foundNode = rootNode
    difference = abs(value - rootNode.value)
    count = 0

    while currParentNodes.qsize() > 0:
        currNode = currParentNodes.get()
        currDifference = abs(value - currNode.value)
        if currDifference < difference:
            difference = currDifference
            foundNode = currNode
        if difference == 0:
            break
        lengthOfChildren = len(currNode.children)
        if(lengthOfChildren > 0):
            for childIndex in range(0,lengthOfChildren):
                currParentNodes.put(currNode.children[childIndex])
        count +=1
    print("Searched through %d nodes" % count)
    return foundNode

# def writeTreeToFile(rootNode, filename):
  
# def getTreeFromFile(filename):
# if __name__ == "__main__":
#     test_breadth_first_nodes()
#     println("")
#     test_depth_first_nodes()