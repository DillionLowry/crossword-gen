﻿# crossword-gen
Builds a crossword given a shape and a wordbank, if possible.

Input: 
1. File with the shape of the puzzle to be made (example shown below).

2. File containing newline delimited words and their definitions.
       
Output: 
1. The puzzle shape
2. a completed puzzle
3. a wordbank

Example shape:
```
---#-
-#---
-----
-##-#
----#
-####
----#
```
The character '-' denotes where a letter will be placed (white space), while the character '#' denotes where a blank is placed (black space).


Time complexity
-------------
worst case is O(M<sup>N</sup>)

where N is the complexity of the puzzle - specifically the number of collisions between
words + 1, with a minimum of N = number of words in the puzzle. Sparse puzzles will have a low n value and dense NYTimes style puzzles
will have a large n value.

M is the number of words in the wordbank. The actual value used will be M/A where A
is an arbitrary value that is determined by the number of words in the wordbank that are the length
of the word to be found.
 
 Example of a puzzle with an N value of 31:
 
|-|-|-| |-|-|-| | |-|
|---|---|---|---|---|---|---|---|---|---|
|-| |-|-|-|-|-| | |-|
|-|-|-|-|-|-|-|-|-|-|
|-| | |-| | | | | |-|
|-|-|-|-| |-|-|-| |-|
|-| | | | |-|-|-| |-|
|-|-|-|-| |-|-|-|-|-|

Example solution:

|u|t|e| |i|t|s| | |l|
|---|---|---|---|---|---|---|---|---|---|
|n| |e|e|r|i|e| | |a|
|c|o|n|v|e|n|t|i|o|n|
|o| | |i| | | | | |g|
|u|r|a|l| |r|a|t| |u|
|t| | | | |a|i|r| |i|
|h|e|e|d| |p|l|e|a|d|

Time taken to solve this puzzle: 0.76 sec

Number of iterations: 254

Because words are chosen randomly, runtime can vary greatly. Out of 10 runs with the puzzle above: 7 were under a second, 9 were under 5 seconds, and one outlier took 68 seconds to find a solution.
