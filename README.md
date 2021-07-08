# BlocksWorldAI
A Blocks World Program inspired from 6.034 MIT AI course(https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/). This program was developed in Python using PyGame. Program can be run on Repl here(https://replit.com/@24sdas/BlocksWorldAI#main.py), though PyGame rendering is often not great. Running the program locally will give better results. 

## Program Theory
This program is based on a environment of blocks that can be manipulated using commands. These commands would then be performed by the computer using a goal tree structure. The goal tree structure enables the computer to gain an intuition of why and how moves are to be made giving it an artificial intelligence feel. In this way, this is in the class of the earliest types of symbolic AI similar to BlocksWorld(https://en.wikipedia.org/wiki/Blocks_world). The goal tree structure can be seen below.

![Goal Tree PNG](https://github.com/Saptak625/BlocksWorldAI/blob/main/ReadMe%20Images/goaltree.png)

### Goal Tree Command Hierachy
### General Operation
These commands all interact with one another by calling on each other in a recursive goal tree. This goal tree can be seen above. The tree delegates specific block operations in a recursive fashion allowing it to solve much more complex problems.
#### Put
The Put Command is a high level command to as it suggests "put a block on top of another block." This is the first command executed on the goal tree when a Manipulating Command is called. This calls on clear top, level, and move respectively. No other command calls this command again as this is used as a master command to prep the blocks in the operation. 

#### Clear Top
The Clear Top Command is a high level command to as it suggests "clear the top of a block." This is called by a Put command to clear the top of the two operation blocks to be able to move them. This calls on itself in case of another block being on top of the block trying to be cleared and get rid respectively.

#### Level
The Level Command is a high level command to as it suggests "level a platform with level of block to stacked on." This called by a Put command to create the platform on which the block to stacked will rest. This is only called if the block to be stacked is 2 wide and the block to be stacked on doesn't have a 2 wide platform to stack on. This calls on a series of move commands to build to the correct level.

#### Get Rid
The Get Rid Command is a high level commmand to as it suggests "get rid of a block to the table." This command is called by the the Clear Top command to rid a block away from the tops of the operation blocks. This calls the move command. 

#### Move
The Move Command is a low level command to as it suggests simply "move a block to a specific location." This command is called by Put, Get Rid, and Level and all goal tree execution chains end on a Move end node as this is the base operation of the recursive goal tree. 


### "Why?" and "How?" Goal Tree Theory
Using a goal tree to stack blocks creates a command chain with the Move Leaf Nodes being the solution to a manipulation command. As the goal tree is a tree, the structure of children and parents allow for the program to answer questions about how and why it performs a specific operation like a human. If you ask the program why it did a certain move, all it has to do is to find the node being questioned and find it's parent(moving up the tree)! On the other hand, if you ask the program how it did a certain move, all it has to do is to find the node being questioned and find it's children(moving down the tree)! How and why operations are implicitly inverse functions!

## Program Usage
This program several commands for different operations:

### Manipulating Commands
This program allows the user to perform manipulating commands on blocks, namely stacking one block onto the other, using the notation "(name of block to be stacked)-->(name of block to be stacked onto)". For example, "b1-->b2". Block sizes doesn't matter, so a 2 wide block can be stacked onto a one wide block given other spot is filled. This is a great example of where the AI is used to think through moves using the goal tree structure.

### "Why?" Commands
Using a goal tree structure allows the program to explain it's choices of moves to perform a manipulation. You can use the notation "why (operation type) (1st block to operate on) (to/on) (2nd block to operate on top of)" for put, move, and level operations, the notation "why rid/get rid (1st block to operate on) to table" for rid operations, and the notation "why clear/clear top (1st block to operate on)" for clear operations. For example, "why put b1 on b2" or "why rid b1 to table" or "why clear top b1."

### "How?" Commands
Using a goal tree structure allows the program to explain it's choices of moves to perform a manipulation. You can use the notation "how (operation type) (1st block to operate on) (to/on) (2nd block to operate on top of)" for put, move, and level operations, the notation "how rid/get rid (1st block to operate on) to table" for rid operations, and the notation "how clear/clear top (1st block to operate on)" for clear operations. For example, "how put b1 on b2" or "how rid b1 to table" or "how clear top b1."

## Test Examples 
### To be added soon!

## Bugs and Fixes
If any bugs are encountered while running this program, which is quite likely given the size of the program, please file an issue.  I will try to address these issues as soon as possible. Any comments or suggestions to improve the code would be much appreciated. The logic for manipulation could definitely be improved in the future. Pull requests are welcome!

