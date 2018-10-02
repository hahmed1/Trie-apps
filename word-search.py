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
        
    def get_children(self):
        return [x for x in self.children if x]

    def has_child(self, letter):
        return letter in self.get_children()

    # look-up an existing child and return it
    def get_child(self, letter):
        if not self.has_child(letter):
            raise ValueError(f'{self} does not have a child with letter {letter}')
    
        pos = _get_pos(letter)
        return self.children[pos]

    def get_child_letters(self):
        print(self.get_children())
        [x.letter for x in self.get_children()]

class Trie:
    def __init__(self):
        self.root = Node('')
    
    def add_word(self, word):

        cur = self.root
        for c in word:
            if not cur.has_child(c):
                node = Node(c)
                cur.add_child(node)
                cur = node
            else:
                cur = cur.get_child(c)

    def print(self):

        dq = deque()
        dq.append(self.root)
        level = 1
        while dq: 
            #print(f'Level: {level}')
            #level += 1

            cur = dq.pop()
            children = cur.get_children()
            child_letters = cur.get_child_letters()

            for c in children: 
                dq.append(c)

            print(f'children: {child_letters}')

#just see if this crashes
def test1():
    word1 = 'dog'
    word2 = 'day'

    t = Trie()
    t.add_word(word1)
    t.add_word(word2)

    #t.print()

    lev1 = t.root.get_children()
    lev2 = []
    for c in lev1:
        print(c.letter)
        lev2.append(c)
    for c in lev2: 
        ch2 = c.get_children()
        for x in ch2: 
            print(x.letter)

test1()