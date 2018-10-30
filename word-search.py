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
    return words



class Node:
    def __init__(self, letter):
        self.letter = letter
        self.children = [None for x in range(26)]
        
        # this gets set to true if the path from root to this node is a valid word 
        self.terminal = False

        self.weight = 0


    # get the position of a new letter in the children array, 
    # irrespective of case
    @staticmethod
    def _get_pos(letter):
        pos = ord(letter.lower()) - 97
        if pos < 0 or pos > 25:
            msg = f'Attempted to add a non alphabetical character {letter}'
            raise ValueError(msg)

        return pos

    # add a single node, which is a letter
    # the node could already be linked with its own children.
    def add_child(self, node):
        new_letter = node.letter

        try:
            position = Node._get_pos(new_letter)

            if self.children[position] == None:
                self.children[position] = node
        except ValueError:
            pass

    # returns non-null raw Node object  
    def get_children(self):
        return [x for x in self.children if x]

    # this is position based
    def has_child(self, letter):

        try:
            pos = Node._get_pos(letter)
            return self.children[pos] != None
        except: 
            return False

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

 
    def increment_weight(self): 
        self.weight += 1

    def get_weight(self):
        return self.weight

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


    # assume that the trie is already built.  
    # we now want to mine large bodies of text and add weights to each node at 
    # each level of the tree.  The basic idea here is to increment the weight by one for each 
    # letter in the word for which we are adding weights.
    #
    # Suppose for example that the word='dog'.  Then for each node in the path "d", "o", "g", 
    # we increment the weight of the node.  
    # TODO: test this

    def add_weight(self, word):
        cur = self.root 
        for idx, c in enumerate(word):
            if not cur.has_child(c):
                return 
            cur.increment_weight()
            cur = cur.get_child(c)

    # Autocomplete feature.  Suggest a list of words based on weights, which are specified according to 
    # the semantics specified in add_weight() above.  
    def suggest_words(self, prefix, num_words=20):
        pass

    def dfs_print_helper(self, source, indent):

        #visited = {self.root: None}

        for node in source.get_children():
            #self.visited[node] = None

            to_print = node.letter.rjust(indent) + '(' + str(node.get_weight()) + ')'

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

    t.print()


def add_word_test():
    words = ['dog', 'DOG', 'day', 'delta', 'dogma', 'A',"to", "tea", "ted", "ten", "i", "in", "inn"]
    
    prefixes = ['dog', 'go', 'a', 'lx', 't', '', 'in', 'x', 'n', 'i']
    expected = [True, False, True, False, True, True, True, False, False, True]
    t = Trie()
    
    for word in words:
        t.add_word(word)

    weights = ['delta', 'dark', 'day', 'deltoid', 'i', 'in']

    for word in weights: 
        t.add_weight(word)

    t.print()


def test2():
    words = create_word_hash('./monte-cristo.txt')

    t = Trie()

    
    for word in words.keys():
        t.add_word(word)


    #t.print()

    import sys

    #looks like it is not finding the size of the full object graph
    print(f"Trie size in Bytes: {sys.getsizeof(t)}")
    print(f'Dict size in MB: {sys.getsizeof(words) / 1024 / 1024}')

    u_input = ''

    while u_input != 'quit':

        u_input = input('>')

        print(t.has_prefix(u_input))

#test2()

add_word_test()


# autocomplete (i.e. for a web form)
# assuming that the source text is a representative
# sample of the word distribution of the English language, the trie can be used to power Autocomplete. 
# 
# 
# Properties of the word-trie: 
#   sparse 
