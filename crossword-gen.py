class Coord(object):
    def __init__(self, start, end, vert):
        self.start = start
        self.end = end
        self.length = (end[0] - start[0]) + (end[1] - start[1]) + 1
        self.vertical = vert

        def __str__(self):
            return self.start, self.end, self.length

class Board(object):
    def __init__(self, shape):
        self.shape = shape
        self.coords = []
        self.width = len(shape[0])
        self.height = len(shape)

    def add_coord(self, coord):
        self.coords.append(coord)

    def get_coords(self):
        return self.coords

    def print_coords(self):
        for coord in self.coords:
            print(coord.start, coord.end, coord.length)

def main():
    #filename = input("Input file name: ")
    filename = "vocab.txt"
    f = open(filename, "r")

    # Wordlist is a 2d list of tuples
    # 0 index is two letter words, max length of 16 letters
    wordlist = [[] for x in range(15)]

    while True:
        word = f.readline().strip()
        definition = f.readline().strip()
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
            ["-","X","X","-","X","X","X","X"],
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

    crossword = Board(test3)

    num_rows = crossword.height
    num_cols = crossword.width

    for r in range(num_rows):
        for c in range(num_cols):
            print(crossword.shape[r][c], end=" ")
        print()

    # find coords

    #l = end - start + 1
    
    for r in range(num_rows):
        start = None
        end = None
        for c in range(num_cols):
            if crossword.shape[r][c]=='-' and not start:
                start = (r,c)
            if (crossword.shape[r][c]=='X' or c == num_cols-1) and start and not end:
                if crossword.shape[r][c]=='X':
                    end = (r,c-1)
                else:
                    end = (r,c)
                h_coord = Coord(start, end, False)
                crossword.add_coord(h_coord)
                start = None
                end = None
            print(r, "  ", c)
        
    print("---------------")

    for c in range(num_cols):
        start = None
        end = None
        for r in range(num_rows):
            if crossword.shape[r][c]=='-' and not start:
                start = (r,c)
            if (crossword.shape[r][c]=='X' or r == num_rows-1) and start and not end:
                if crossword.shape[r][c]=='X':
                    end = (r-1,c)
                else:
                    end = (r,c)
                v_coord = Coord(start, end, True)
                crossword.add_coord(v_coord)
                start = None
                end = None
            print(r, "  ", c)

    #print(crossword.get_coords())

    crossword.print_coords()



    tried_words = set()
    #try to place word
    #check surroundings
    #attempt to place crossing words


if __name__ == "__main__":
    main()

