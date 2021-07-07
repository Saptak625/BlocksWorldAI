# BlocksWorldAI
A Blocks World Program inspired from 6.034 MIT AI course(https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/). This program was developed in Python using PyGame.

## Program Theory
This program is based on a environment of blocks that can be manipulated using commands. These commands would then be performed by the computer using a goal tree structure. The goal tree structure enables the computer to gain an intuition of why and how moves are to be made giving it an artificial intelligence feel. In this way, this is in the class of the earliest types of symbolic AI similar to BlocksWorld(https://en.wikipedia.org/wiki/Blocks_world). A version of the goal tree structure can be seen below.

## Program Usage
This program several commands for different operations:

### Manipulating Commands
This program allows the user to perform manipulating commands on blocks, namely stacking one block onto the other, using the notation "(name of block to be stacked)-->(name of block to be stacked onto)". For example "b1-->b2". Block sizes doesn't matter, so a 2 wide block can be stacked onto a one wide block given other spot is filled. This is a great example of where the AI is used to think through moves using the goal tree structure. Examples are to be added to this documentation in the future.

### "Why?" Commands
Using a goal tree structure allows the program to explain it's choices of moves to perform a manipulation. You can use the notation "why (operation type) (1st block to operate on) (to/on) (2nd block to operate on top of)" for put, move, and level operations and the notation "why (operation type) (1st block to operate on)" for rid and clear operations. 

#Rest of Documentation to come soon!
