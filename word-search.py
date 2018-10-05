from collections import deque
import pdb
#read the book, get the unique words

def create_word_hash(text):   
    words = {}
    distinct_count = 0
    with open(text, 'r') as book: 
        for line in book: 
            for word in line.split():
                if word not in words: 
                    words[word] = 1
                    distinct_count += 1
    print(f"distinct word count {distinct_count}")




class Node:
    def __init__(self, letter):
        self.letter = letter
        self.children = [None for x in range(26)]
        
        # this gets set to true if the path from root to this node is a valid word 
        self.terminal = False

    # get the position of a new letter in the children array, 
    # irrespective of case
    @staticmethod
    def _get_pos(letter):
        pos = ord(letter.lower()) - 97
        if pos < 0 or pos > 25: 
            raise ValueError(f'Attempted to add a non alphabetical character {letter}')

        return pos

    # add a single node, which is a letter
    # the node could already be linked with its own children.
    def add_child(self, node):
        new_letter = node.letter

        position = Node._get_pos(new_letter)

        if self.children[position] == None:
            self.children[position] = node

    # returns non-null raw Node object  
    def get_children(self):
        return [x for x in self.children if x]

    # this is position based
    def has_child(self, letter):

        pos = Node._get_pos(letter)
        return self.children[pos] != None

        #return letter in self.get_children()

    # look-up an existing child and return it
    def get_child(self, letter):
        if not self.has_child(letter):
            raise ValueError(f'{self} does not have a child with letter {letter}')
    
        pos = Node._get_pos(letter)
        return self.children[pos]


    def get_child_letters(self):
        #print(self.get_children())
        #pdb.set_trace()
        
        return [x.letter for x in self.get_children()]

class Trie:
    def __init__(self):
        self.root = Node('')
      

    def add_word(self, word):
        #pdb.set_trace()
        cur = self.root
        for idx,c in enumerate(word):
            if not cur.has_child(c):
                node = Node(c)
                cur.add_child(node)
                cur = node
            else:
                cur = cur.get_child(c)
            
            if idx == len(word) - 1:
                cur.terminal = True

    def dfs_print_helper(self, source, indent):

        #visited = {self.root: None}

        for node in source.get_children():
            #self.visited[node] = None

            to_print = node.letter.rjust(indent)

            if node.terminal == True:
                to_print +='.'

            print(to_print)
            self.dfs_print_helper(node, indent+2)

    # print that traverses using DFS
    def print(self):
        #self.visited = {self.root : None}

        self.dfs_print_helper(self.root, 0)

    
    
def test1():
    words = ['dog', 'DOG', 'day', 'delta', 'damn', 'dogma', 'god', 'A',"to", "tea", "ted", "ten", "i", "in", "inn"]
    
    t = Trie()
    
    for word in words:
        t.add_word(word)

    t.print()

    

test1()