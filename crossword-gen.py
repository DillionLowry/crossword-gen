import random
import re
import string
from copy import deepcopy

class Coord(object):
    def __init__(self, start, end, vert, num):
        self.start = start
        self.end = end
        self.length = (end[0] - start[0]) + (end[1] - start[1]) + 1
        self.vertical = vert
        self.number = num
        self.collisions =[]

    def __str__(self):
        return str(self.start)+ str(self.end)+ " "+str(self.number)+" "+self.get_direction()
    
    def get_direction(self):
        if self.vertical:
            return "down"
        else:
            return "across"


class Word(object):
    def __init__(self, coord, word_tuple):
        self.coord = coord
        self.text = word_tuple[0]
        self.clue = word_tuple[1]

    def __str__(self):
        return self.text

class Board(object):
    def __init__(self, shape):
        self.shape = shape
        self.generated = shape
        self.coords = []
        self.width = len(shape[0])
        self.height = len(shape)
        self.collision_list = []

    def add_coord(self, coord):
        self.coords.append(coord)

    def get_coords(self):
        return self.coords

    def print_coords(self):
        for coord in self.coords:
            print(coord.start, coord.end, coord.length, coord.number, coord.get_direction())
            for ccoord in coord.collisions:
                print(ccoord)
    
    def print_board(self):
        for row in self.generated:
            for item in row:
                print(str(item)[0], end='')
            print()

def generate_coordinates(crossword):
    num_rows = crossword.height
    num_cols = crossword.width
    '''
    for r in range(num_rows):
        for c in range(num_cols):
            print(crossword.shape[r][c], end=" ")
        print()
    '''
    horizontal_num = 1
    vertical_num = 1


    # find coords by row
    for r in range(num_rows):
        start = None
        end = None
        for c in range(num_cols):
            # start a new word
            if crossword.shape[r][c]=='-' and not start:
                # it isn't just one character
                if c+1 < num_cols and crossword.shape[r][c+1] != 'X':
                    start = (r,c)
                    crossword.shape[r][c]=horizontal_num
                else:
                    continue
            # continue word
            if start and not end:
                crossword.shape[r][c]=horizontal_num
                # This is the last letter
                if (c+1==num_cols or crossword.shape[r][c+1]=='X'):
                        end = (r,c)
                        h_coord = Coord(start, end, False, horizontal_num)
                        crossword.add_coord(h_coord)
                        horizontal_num+=1
                        start = None
                        end = None
                        continue
                #print(r, "  ", c)
        
    #print("---------------")

    # find coords by col
    for c in range(num_cols):
        start = None
        end = None
        for r in range(num_rows):
             # start a new word, either the across number or '-'
            if (isinstance(crossword.shape[r][c], int) or crossword.shape[r][c]=='-') and not start:
                # it isn't just one character
                if r+1 < num_rows and crossword.shape[r+1][c] != 'X':
                    start = (r,c)
                else:
                    continue
            # continue word
            if start and not end:
                # This is the last letter
                if (r+1==num_rows or crossword.shape[r+1][c]=='X'):
                        end = (r,c)
                        v_coord = Coord(start, end, True, vertical_num)

                        # collisions
                        for x in range(start[0],end[0]+1):
                            if (isinstance(crossword.shape[x][c], int)):
                                crossword.coords[crossword.shape[x][c]-1].collisions.append(v_coord)
                                v_coord.collisions.append(crossword.coords[crossword.shape[x][c]-1])
                        crossword.add_coord(v_coord)
                        vertical_num+=1
                        start = None
                        end = None
                        continue
            #print(r, "  ", c)

def generate_collisions(board, coord):
    ''' old method
    collision_list = [board.coords[0]]
    for coord in board.coords[0].collisions:
        collision_list.append(coord)
    for coord in collision_list:
        for col in coord.collisions:
            if col and col not in collision_list:
                collision_list.append(col)
    return collision_list
    '''
    if coord not in board.collision_list:
        #print("generating ",coord)
        board.collision_list.append(coord)
        for coll in coord.collisions:
            generate_collisions(board,coll)
    else:
        return

def generate_crossword(board, wordlist):
    
    tried_words = set()
    colls = []

    #place first word
    #place_word(board, board.coords[0], wordlist, None)
    '''
    for coord in board.coords[0].collisions:
        collision_list.append(coord)
    
    for coord in collision_list:
        
        for coll in coord.collisions:
            if coll not in collision_list:
                print('Added: ', coord)
                collision_list.append(coll)
    
    '''
    #completed = True
    #completed = find_spot(board, board.coords[0], collision_list, wordlist)
    #print(completed)
    #colls=generate_collisions(board, board.coords[0])
    #board = find_and_place2(board, board,colls,wordlist)
    generate_collisions(board, board.coords[0])
    colls = board.collision_list

    find_and_place(board,board,colls,wordlist)

    #for coord in colls:
        #print("c- ", coord)
    return board
    
def find_and_place(board, new_board, collision_list, wordlist):

    if len(collision_list) > 0:
        print("----------START --------------",collision_list[0],"LENGTH:",len(collision_list))

    found = False
    copy = deepcopy(new_board)

    # we handled all collisions
    if collision_list==[]:
        print("MADE IT TO EMPTY LIST")
        board.generated = new_board.generated
        return True

    constraints = ""
    # only add the first character of the constraint in the case that it is a two+ digit number
    for x in range(collision_list[0].length):
        if collision_list[0].vertical:
            constraints += str(copy.generated[collision_list[0].start[0]+x][collision_list[0].start[1]])[0]
        else:
            constraints += str(copy.generated[collision_list[0].start[0]][collision_list[0].start[1]+x])[0]
    print("constraints are:", constraints)

    # Generate regex from the constraints
    regex = ""
    for char in constraints:
        if char in string.ascii_lowercase:
            regex+=char
        else:
            regex+="."
    print(regex)
    found_matches = [word for word in wordlist[len(constraints)-2] if re.match(regex, word[0]) is not None]

    for word in found_matches:
        # place the word down
        for x in range(collision_list[0].length):
            #print(x)
            #print(word[0][x])
            #print(collision_list[0].start[0], " ", collision_list[0].start[1])
            if collision_list[0].vertical:
                copy.generated[collision_list[0].start[0]+x][collision_list[0].start[1]] = word[0][x]
            else:
                copy.generated[collision_list[0].start[0]][collision_list[0].start[1]+x] = word[0][x]
            
        copy.print_board()
        found = find_and_place(board,copy,collision_list[1:], wordlist)
        if found:
            print("-------------------------------------------------------------------- found")
            return True
        print("Returning False for:",word)
    return False



def find_spot(board, coord, collision_list, wordlist):
    placed = False
    attemps_to_place=0

    print("FINDING A SPOT")
    print(coord)
    if coord == None:
        return
    for col in coord.collisions:
        if col and col not in collision_list:
            #all_placed = False
            collision_list.append(col)
            find_spot(board, col, collision_list, wordlist)
    while not placed and attemps_to_place <100:
        tried_words=[]
        constraints = ""
        # only add the first character of the constraint in the case that it is a two+ digit number
        for x in range(coord.length):
            if coord.vertical:
                constraints += str(board.generated[coord.start[0]+x][coord.start[1]])[0]
            else:
                constraints += str(board.generated[coord.start[0]][coord.start[1]+x])[0]
        print("constraints are: ", constraints)

        placed, tried_words = place_word(board,coord,wordlist, constraints, tried_words)
        attemps_to_place+=1
    return placed
   
def place_word(board, coord, words, constraints, tried):
    if constraints==None:
        print(coord.length)
        word = words[coord.length-2][random.randrange(len(words[coord.length-2]))]
    else:
        # Generate regex from the constraints
        regex = "^"
        for char in constraints:
            if char in string.ascii_lowercase:
                regex+=char
            else:
                regex+="."
        print(regex)
        found_matches = [word for word in words[len(constraints)-2] if re.match(regex, word[0]) is not None]
        '''
        for match in found_matches:
            print(match)
            print(type(match))
        '''
        # no matches found, or all tried and failed
        if len(found_matches)==0 or len(found_matches)==len(tried):
            print("Didn't find any matches")
            return False, tried
        print("num matches found ",len(found_matches))
        #TODO, CHECK THAT THE WORD WORKS AND HASN'T BEEN TRIED BEFORE
        word = found_matches[random.randrange(len(found_matches))]
        while word in tried:
            word = found_matches[random.randrange(len(found_matches))]
        tried.append(word)
        
    print("THE FOUND WORD IS: ",word)
    for x in range(coord.length):
        #print(x)
        print(word[0][x])
        print(coord.start[0], " ", coord.start[1])
        if coord.vertical:
            board.generated[coord.start[0]+x][coord.start[1]] = word[0][x]
        else:
            board.generated[coord.start[0]][coord.start[1]+x] = word[0][x]

    board.print_board()

    return True, tried


def main():
    #filename = input("Input file name: ")
    filename = "words2.txt"
    f = open(filename, "r")

    # Wordlist is a 2d list of tuples
    # 0 index is two letter words, max length of 16 letters at index 14
    wordlist = [[] for x in range(15)]

    #while True:
    for x in range(128000):
        try:
            word = f.readline().strip().lower()
        except:
            continue
        if len(word) <2 or len(word) > 14:
            continue
        #definition = f.readline().strip()
        definition = "Testing values"
        if not word:
            break
        wordlist[len(word)-2].append((word,definition))

    # Sort all words within each wordlength
    for words in wordlist:
        words.sort()
    '''
    for word in wordlist[3]:
        print(word)
    '''

    test = ["----x---",
            "----x---",
            "--------",      
            "xxxxx---",  
            "-----xxx",   
            "--------",
            "----x---",
            "----x---"
            ]

    test2 = ["----x---",
            "----x---",
            "--------",      
            "xxxxx---",
            ]

    test3 = [["-","-","-","X","X","-","-","-"],
            ["-","-","-","X","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","X","X","-","X","-","X","X"],
            ["-","-","-","X","X","-","-","-"],
            ["-","-","-","-","X","-","-","-"],
            ["-","-","-","-","X","-","-","-"]]

    test4 = [["-","-","-","X","X"],
            ["-","X","X","-","-"],
            ["-","-","-","-","-"],
            ["-","X","X","-","X"],
            ["-","-","-","-","X"],
            ["-","X","X","X","X"],
            ["-","-","-","-","X"]]

    test5 = [["-","-","-","-","X","X","-","-","-","-","X","-","-","-","-",],
            ["-","-","-","-","-","X","-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","X","-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-","-","-","-","-","-","X",],
            ["-","-","-","-","-","-","-","X","X","X","X","-","-","-","-",],
            ["X","X","X","-","-","-","X","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","X","-","-","-","-","-","-","X","-","-","-",],
            ["-","-","-","X","-","-","-","-","-","-","-","X","-","-","-",],
            ["-","-","-","X","-","-","-","-","-","-","X","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","X","-","-","-","X","X","X",],
            ["-","-","-","-","X","X","X","X","-","-","-","-","-","-","-",],
            ["X","-","-","-","-","-","-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-","X","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-","X","-","-","-","-","-",],
            ["-","-","-","-","X","-","-","-","-","X","X","-","-","-","-",]]

    crossword = Board(test5)
    generate_coordinates(crossword)
    crossword.print_coords()
    crossword.print_board()
    generate_crossword(crossword, wordlist)    
    crossword.print_board()





if __name__ == "__main__":
    main()