import random
import re
import string
from copy import deepcopy
import time
import argparse
start_time = time.time()

class Coord(object):
    def __init__(self, start, end, vert, num):
        self.start = start  # tuple coordinate
        self.end = end      # tuple coordinate
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
    
    def get_number(self):
        return self.number

class Word(object):
    def __init__(self, coord, word_tuple):
        self.coord = coord
        self.text = word_tuple[0]
        self.clue = word_tuple[1]

    def __str__(self):
        return self.text+"-"+self.clue

class Board(object):
    def __init__(self, shape, debug=False):
        self.shape = shape  # board layout with symbols
        self.generated = shape  # board with
        self.coords = []
        self.width = len(shape[0])
        self.height = len(shape)
        self.collision_list = []
        self.debug = debug
        self.iterations = 0
        self.wordlist = []

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
        for row in self.shape:
            print("|",end="")
            for item in row:
                if str(item)[0]=="#":
                    print(" ",end="|")
                else:
                    print("-", end='|')
            print()
        print()

    def print_solution(self):
        #print the board
        for row in self.generated:
            print("|",end="")
            for item in row:
                if str(item)[0]=="#":
                    print(" ",end="|")
                else:
                    print(str(item)[0], end='|')
            print()
        print()

        # print words
        for word in self.wordlist[::-1]:
            print(word.coord.get_number(), word.coord.get_direction(), "-", word.text)

    def print_clues(self):
        for word in self.wordlist[::-1]:
            print(word.coord.get_number(), word.coord.get_direction(), "-", len(word.text), "letters -",word.clue)

    def print_iterations(self):
        if self.debug:
            print("Number of iterations:",self.iterations)
        else:
            print("Run in debug mode to track iterations")
    
    def print_complexity(self):

        # divide by two because each coord saves it's collision with each other ex 1->2, 2->1
        print("Complexity of this crossword:", int(sum(len(coord.collisions) for coord in self.coords)/2)+1)


def generate_coordinates(crossword):
    num_rows = crossword.height
    num_cols = crossword.width
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
                if c+1 < num_cols and crossword.shape[r][c+1] != '#':
                    start = (r,c)
                    # place the horizontal number to be used for collision checking
                    crossword.shape[r][c]=horizontal_num
                else:
                    continue
            # continue word
            if start and not end:
                crossword.shape[r][c]=horizontal_num
                # This is the last letter
                if (c+1==num_cols or crossword.shape[r][c+1]=='#'):
                        end = (r,c)
                        h_coord = Coord(start, end, False, horizontal_num)
                        crossword.add_coord(h_coord)
                        horizontal_num+=1
                        start = None
                        end = None
                        continue
        
    # find coords by col
    for c in range(num_cols):
        start = None
        end = None
        for r in range(num_rows):
             # start a new word, either the across number or '-'
            if (isinstance(crossword.shape[r][c], int) or crossword.shape[r][c]=='-') and not start:
                # it isn't just one character
                if r+1 < num_rows and crossword.shape[r+1][c] != '#':
                    start = (r,c)
                else:
                    continue
            # continue word
            if start and not end:
                # This is the last letter
                if (r+1==num_rows or crossword.shape[r+1][c]=='#'):
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

# recursively gets collisions, typical usage starts at coords[0]
def generate_collisions(board, coord):
    if coord not in board.collision_list:
        if board.debug:
            print("generating ",coord)
        board.collision_list.append(coord)
        for coll in coord.collisions:
            generate_collisions(board,coll)
    else:
        return

def generate_crossword(board, wordlist):
    
    board.print_board()
    generate_coordinates(board)
    generate_collisions(board, board.coords[0])
    colls = board.collision_list
    if not find_and_place(board,board,colls,wordlist):
        print("Could not generate a crossword with the given wordlist")
        exit()
    board.print_clues()
    if board.debug:
        board.print_complexity()

    return board

# recursively places words down until no more collision exist
def find_and_place(board, new_board, collision_list, wordlist):
    if board.debug:
        board.iterations +=1
        if len(collision_list) > 0:
            print("START:",collision_list[0],"LENGTH:",len(collision_list))

    found = False
    copy = deepcopy(new_board)

    # we handled all collisions
    if collision_list==[]:
        board.generated = new_board.generated
        return True

    constraints = ""
    # only add the first character of the constraint in the case that it is a two+ digit number
    for x in range(collision_list[0].length):
        if collision_list[0].vertical:
            constraints += str(copy.generated[collision_list[0].start[0]+x][collision_list[0].start[1]])[0]
        else:
            constraints += str(copy.generated[collision_list[0].start[0]][collision_list[0].start[1]+x])[0]

    # Generate regex from the constraints
    regex = ""
    for char in constraints:
        if char in string.ascii_lowercase:
            regex+=char
        else:
            regex+="."

    if board.debug:
        print("constraints are:", constraints,"->",regex, "Iteration:", board.iterations)

    found_matches = [word for word in wordlist[len(constraints)-2] if re.match(regex, word[0]) is not None]

    random.shuffle(found_matches)

    for word in found_matches:
        # place the word down
        for x in range(collision_list[0].length):
            if collision_list[0].vertical:
                copy.generated[collision_list[0].start[0]+x][collision_list[0].start[1]] = word[0][x]
            else:
                copy.generated[collision_list[0].start[0]][collision_list[0].start[1]+x] = word[0][x]
        
        if board.debug:
            copy.print_solution()

        # pass this iteration on and try to fit the next collision
        found = find_and_place(board,copy,collision_list[1:], wordlist)

        # All iterations down this path worked, so confirm the word
        if found:
            fitting_word = Word(collision_list[0], word)
            board.wordlist.append(fitting_word)
            return True
        elif board.debug:
            print("Returning False for:",word)
    return False

def import_words(filename, wordlist, has_definitions):
    try:
        f = open(filename, "r", encoding="utf-8")
        lines = f.readlines()

        if has_definitions:
            for word, definition in zip(lines[0::2], lines[1::2]):
                if len(word) <2 or len(word) > 20:
                    continue
                wordlist[len(word.strip())-2].append((word.strip(),definition.strip()))
        else:
            definition = "Testing values"
            for word in lines:
                if len(word) <2 or len(word) > 20:
                    continue
                wordlist[len(word.strip())-2].append((word.strip(),definition))
        f.close()
    except Exception as e:
        print(e)

def import_shape(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]

        if len(lines) < 2 or is_jagged(lines):
            print("The Puzzle is incorrectly drawn.")
            exit()

        if len(lines) > 50:
            print("Warning: Puzzles this large may take a very, VERY, long time to finish.")
        
        shape = [[] for x in range(len(lines))]
        for x in range(len(lines)):
            for char in lines[x]:
                #TODO: symbol checking
                shape[x].append(char)

        return shape

    except Exception as e:
        print(e)

def is_jagged(twod_list):
    try:
        for row in twod_list:
            if len(row.strip()) != len(twod_list[0].strip()):
                return True
        return False
    except Exception as e:
        print(e)
    

def main(args):

    if (args.s and args.w):
        shapefile = args.s
        wordfile = args.w
        has_definitions = args.no_defs
        debug_mode = args.debug
    else:
        print("Please include files. See '--help'")
        exit()


    # Wordlist is a 2d list of tuples
    # 0 index is two letter words
    wordlist = [[] for x in range(20)]

    import_words(wordfile, wordlist, has_definitions)

    shape = import_shape(shapefile)
    crossword = Board(shape, debug_mode)
    generate_crossword(crossword, wordlist)   
    crossword.print_solution()

    print("Time taken:",time.time() - start_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', type=str, help="File to import shape from")
    parser.add_argument('--w', type=str, help="File to import wordbank from")
    parser.add_argument('--no_defs', action='store_false', help="Wordbank does not include definitions")
    parser.add_argument('--debug', action='store_true', help="Print additional information, including iterations")
    args = parser.parse_args()
    main(args)
