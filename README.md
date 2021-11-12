# crossword-gen
 
Time complexity, worst case, is O(M^N)

where N is the complexity of the puzzle - specifically the number of collisions between
words. Sparse puzzles will have a low n value and dense NYTimes style puzzles
will have a large n value

M is the number of words in the wordbank. The actual value used will be M/A where A
is an arbitrary value that is determined by the number of words in the wordbank that are the length
of the word to be found.
 
 Example of a puzzle with an N value of 41:
 
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
