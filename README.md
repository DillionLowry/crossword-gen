# crossword-gen
Builds a crossword given a shape and a wordbank or through the use of the XWord Info API to fetch words from past NYT crosswords.

Input: 
-------
1. File with the shape of the puzzle to be made (example shown below).
2. File containing newline delimited words and their definitions AND/OR --xword command
       
Output: 
------
1. The puzzle shape
2. a completed puzzle
3. a wordbank

API:
-----
More info on the XWord Info API can be found here:
https://www.xwordinfo.com/ and
https://www.xwordinfo.com/JSON/
Note: Neither I nor xwordinfo own the data returned from the API. 
Read more here: https://xwordblog.com/2021/03/11/can-i-have-your-data/
Example shape:
-------
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

Usage
------------
This program uses the argparse module for command line arguments.

--s FILENAME -       Required - File to import shape from

--w FILENAME -       Required - File to import wordbank from

--no_defs -          (flag) Wordbank does not include definitions

--debug -            (flag) Print additional information, including iterations

 --xword * -         Import words from the Xcode Info API. Can be given start/end dates in format YYYY/MM/DD
 
       Usage: --xword                     - 10 days of words starting at a random date
              --xword STARTDATE           - 10 days of words starting at given date
              --xword STARTDATE ENDDATE   - Get all words between the given dates

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
