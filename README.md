# Nurikabe solver

## What is a nurikabe puzzle?
Each puzzle consists of a grid containing clues in various places. The objective is to create islands by partitioning between clues with walls so:

+ Each island contains exactly one clue.
+ The number of squares in each island equals the value of the clue.
+ All islands are isolated from each other horizontally and vertically.
+ There are no wall areas of 2x2 or larger.
+ When completed, all walls form a continuous path.

## Program
The program is run by typing

    python3 main.py [file-name] [timer(optional)]

And the solution is written in the file. If you wish, you can add a *timer* (default is 0) to see how the program is trying to find a solution (progress is printed to console).
