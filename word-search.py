from collections import deque

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

    def is_terminal(self):
        return self.terminal

    # sets terminal to true
    def set_terminal(self):
        self.terminal = True

class Trie:
    def __init__(self):
        self.root = Node('')
      

    def add_word(self, word):
        cur = self.root
        for idx,c in enumerate(word):
            if not cur.has_child(c):
                node = Node(c)
                cur.add_child(node)
                cur = node
            else:
                cur = cur.get_child(c)

            # set the last letter to a terminal node
            if idx == len(word) - 1:
                cur.set_terminal()

    def dfs_print_helper(self, source, indent):

        #visited = {self.root: None}

        for node in source.get_children():
            #self.visited[node] = None

            to_print = node.letter.rjust(indent)

            if node.is_terminal():
                to_print +='.'

            print(to_print)
            self.dfs_print_helper(node, indent+2)

    # print that traverses using DFS
    def print(self):
        #self.visited = {self.root : None}

        self.dfs_print_helper(self.root, 0)

    def has_prefix(self, prefix):
        return self.has_prefix_helper(prefix, self.root.get_children())

    def has_prefix_helper(self, prefix, node_list):

        if prefix == '':
            return True

        else:
            cur_letter = prefix[0].lower()

            trie_letters = [x.letter.lower() for x in node_list]

            if cur_letter in trie_letters:

                # 2nd argument finds the matching node object and recurses 
                return self.has_prefix_helper(prefix[1:], [x for x in node_list if x.letter.lower() == cur_letter.lower()][0].get_children())
            else:
                return False

                
            
            
    
    
def test1():
    words = ['dog', 'DOG', 'day', 'delta', 'dogma', 'A',"to", "tea", "ted", "ten", "i", "in", "inn"]
    
    prefixes = ['dog', 'go', 'a', 'lx', 't', '', 'in', 'x', 'n', 'i']
    expected = [True, False, True, False, True, True, True, False, False, True]
    t = Trie()
    
    for word in words:
        t.add_word(word)

    tests_pass = True
    for i,test in enumerate(prefixes):

        result = t.has_prefix(test)

        print(f'Contains prefix: {test}: {result}.  Expected: {expected[i]}')

        if result != expected[i]:
            tests_pass = False
    
    print(f'tests pass: {tests_pass}')
    

test1()