# Nurikabe solver

## What is a nurikabe puzzle?

Each puzzle consists of a grid containing clues in various places. The objective is to create islands by partitioning between clues with walls so:

+ Each island contains exactly one clue.
+ The number of squares in each island equals the value of the clue.
+ All islands are isolated from each other horizontally and vertically.
+ There are no wall areas of 2x2 or larger.
+ When completed, all walls form a continuous path.

Each puzzle will be represented as a 2 dimentional matrix where each element is either a digit (0-9) or a wall ('#') or an empty space ('.').

## Use of the program

1. Code -> Download zip.
2. Extract into a folder.
3. Copy your text file containing the unsolved board into the [puzzles](./puzzles) directory (an example of a valid puzzle can be found in [this file](./test1.txt)).
4. The program is run by typing
    
    python3 main.py [file-name] [timer(optional)]

    Where *file-name* is the name of the file where you have copied the puzzle. Furthermore, the solution is written in the file beneath the existing unsolved board. If you wish, you can add a *timer* (default is 0) to see how the program is trying to find a solution (progress is printed to console).
