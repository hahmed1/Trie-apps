import argparse


class Node:
    def __init__(self, letter):
        self.letter = letter

        self.children = [None for x in range(26)]
        
        # this gets set to true if the path from root to this node is a valid word 
        self.terminal = False

        self.weight = 0

     
    def __repr__(self):
        return f'Node object - Letter: {self.letter} - Weight:{self.weight}'

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

    # either returns the immediate child with the given letter, or null
    def lookup(self, letter):
        return self.children[Node._get_pos(letter)]


class Trie:
    def __init__(self, num_suggest):
        self.root = Node('')
        self.num_suggest = num_suggest
        self.suggest_visited = {}      

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
    # 
    # -> Tests reveal that the below method works, except that the last letter of the word does not get 
    #    incremented, which doesn't affect the suggestion feature.  

    def add_weight(self, word):
        cur = self.root 
        for idx, c in enumerate(word):
            if not cur.has_child(c):
                return 
            cur.increment_weight()
            cur = cur.get_child(c)

    # basically a DFS
    def suggest_helper(self, prefix, source):
        
        if len(self.suggest_visited) >= self.num_suggest:
            return

        children = sorted(source.get_children(), key=lambda y: y.weight, reverse=True)
        
        if children:
            for node in children:

                if node.is_terminal():
                    self.suggest_visited[prefix + node.letter] = 1
                else:
                    self.suggest_helper(prefix + node.letter, node)
                


    def suggest(self, prefix):

        cur = self.root
        pos = 0

        #advance 'cur' to point to the lowest node in the Trie that matches with the prefix
        while cur and pos < len(prefix): 
            cur = cur.get_child(prefix[pos])
            pos += 1

    
        self.suggest_visited.clear()
        self.suggest_helper(prefix, cur)
        
        return list(self.suggest_visited.keys())


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


    def has_prefix_helper(self, prefix):
        cur_node = self.root
        cur_letter = 0
        prefix_len = len(prefix)
        while cur_node != None and cur_letter < prefix_len:
            cur_node = cur_node.lookup(prefix[cur_letter])
            cur_letter += 1

        #pdb.set_trace()
        if cur_letter == prefix_len and cur_node != None:
            return True
        else:
            return False



    def has_prefix(self, prefix):
        #return self.has_prefix_helper(prefix, self.root.get_children())
        return self.has_prefix_helper(prefix)
    
                 
def add_weights_test():
    words = ['dog', 'DOG', 'day', 'delta', 'dogma', 'A',"to", "tea", "ted", "ten", "i", "in", "inn"]
    
    prefixes = ['dog', 'go', 'a', 'lx', 't', '', 'in', 'x', 'n', 'i']
    expected = [True, False, True, False, True, True, True, False, False, True]
    t = Trie(20)
    
    for word in words:
        t.add_word(word)

    weights = ['delta', 'dark', 'day', 'deltoid', 'i', 'in']

    for word in weights: 
        t.add_weight(word)

    t.print()

def suggestion_test():
    words = ['dog', 'drake', 'dragon', 'detla', 'day']

    t = Trie(20)
    
    for word in words:
        t.add_word(word)

    weights = ['drake'] * 7
    weights.append('dragon')
    
    weights.append('dog')
    weights.append('dog')

    for i in range(6):
        weights.append('day')

    weights.append('delta')

    for word in weights: 
        t.add_weight(word)

    #t.suggest_words('de')
    t.print()

    print(t.suggest('d'))



def build_trie(path_to_text, num_suggest):
    words = {}
    distinct_count = 0

    trie = Trie(num_suggest)  
    with open(path_to_text, 'r') as text:
        for line in text: 
            for word in line.split():

                # use the words dict to add the current word to the trie 
                # only if we have not yet seen it
                if word not in words:
                    words[word] = 1
                    distinct_count += 1
                    trie.add_word(word)
                
                # update the trie weight regardless of whether 
                # we have seen yet or not, so that weights approximate 
                # English word frequencies to help with the auto-complete feature
                trie.add_weight(word)

    print(f"distinct word count {distinct_count}")
    return trie   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide a source of text, provide a prefix, and get a list of autocomplete-suggestions for the prefix based on the provided text')
    parser.add_argument('-text', '-t',  help='the path to the source text with which we will build the word-frequence trie', required=True)
    parser.add_argument('-prefix', '-p', help='the prefix (i.e. key) to the trie',required=True)
    parser.add_argument('-count', '-c' ,help='the number of words to return in the suggestion list', default=20)
    args = parser.parse_args()

    trie = build_trie(args.text, args.count)
    words = trie.suggest(args.prefix)
    for word in words:
        print(word)


