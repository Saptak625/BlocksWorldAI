#Pygame Screen
import pygame
from pygame.locals import *
import sys
import time
from multipledispatch import dispatch 
from graphviz import Digraph
pygame.init()
display_width = 800
display_height = 800
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
blue = (0, 0, 255)
gameDisplay= pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Block Stacking')
clock = pygame.time.Clock()
FPS=500

#Classes and Variables
global goalTreeDict
goalTreeDict={}
class GoalTree():
	def __init__(self, rootTask, movetype="put on"):
		rootNode=GoalTreeNode(rootTask, movetype)
		moveString=movetype+" "+str(rootNode.taskStart)+"-->"+str(rootNode.taskEnd)
		goalTreeDict[moveString]=rootNode
	def addNode(self, task, movetype, parent):
		#Note that parent node is required and NOT pointer
		node=GoalTreeNode(task, movetype, parent)
		moveString=node.moveType+' '+str(node.taskStart)+"-->"+str(node.taskEnd)
		if moveString in goalTreeDict:
			return goalTreeDict[moveString]
		else:
			goalTreeDict[moveString]=node
			parent.addChild(node)
			goalTreeDict[parent.createKey()]=parent
			return node

class GoalTreeNode():
	#Constructor
	def __init__(self, task, movetype, parent=None):
		#Note that task is a tuple of size two that is preprocessed for the blocks
		self.children=[]
		if not isinstance(task, tuple) and movetype=='clear top':
			self.taskStart=task
			self.taskEnd=None
		else:
			self.taskStart=task[0]
			self.taskEnd=task[1]
		self.moveType=movetype
		if parent==None:
			self.parent=None
		else:
			self.parent=parent.createKey()
	def createKey(self):
		return self.moveType+' '+str(self.taskStart)+"-->"+str(self.taskEnd)
	def addChild(self, child):
		#Note that the children pointers are appended
		self.children.append(child.createKey())

	def __repr__(self):
		return f"(--->Children: {str(self.children)} --->Parent: {str(self.parent)} --->Move: [{str(self.taskStart)+'->'+str(self.taskEnd)}] --->MoveType: {self.moveType})"

class Block():
	colors=red, blue, green
	colorIndex=0
	def __init__(self, size, place, name, color=None):
		self.size=size
		self.place=[place+i for i in range(size[0])]
		self.name=name
		self.blocksAbove=[]
		self.height=0
		if color==None:
			Block.colorIndex+=1
			self.color=Block.colors[Block.colorIndex%3]
		else:
			self.color=color
	def resetColorIndex():
		Block.colorIndex=0
	def __repr__(self):
		return f"(--->Size of Block: {self.size}--->Positions: {self.place}--->Blocks Above: {self.blocksAbove})"

def textboxInput(text=""):
	text = text
	font = pygame.font.SysFont(None, 30)
	img = font.render(text, True, black)
	rect = img.get_rect()
	rect.topleft = (20, 20)
	cursor = Rect(rect.topright, (3, rect.height))
	gameDisplay.blit(img, rect)
	if time.time() % 1 > 0.5:
		pygame.draw.rect(gameDisplay, black, cursor)

class Table():
	def __init__(self, table_size):
		self.size=table_size
		self.blockPos=[ 0 for key in range(table_size)]
		self.blocks={}

	def addBlock(self, block):
		if isinstance(block, Block):
			pass
		elif isinstance(block, list) and len(block)==3:
			#Block details are provided
			block=Block(block[0], block[1], block[2])
		elif isinstance(block, list) and len(block)==4:
			#Block details are provided
			block=Block(block[0], block[1], block[2], color=block[3])
		else:
			sys.exit("Parameters given are not of right type")
		#Block is created
		highestValue=0
		counter=0
		for place in block.place:
			if self.blockPos[place-1]>highestValue:
				highestValue=self.blockPos[place-1]
				counter+=1
		if counter>1:
			sys.exit("This block is not on a flat surface.")
		block.height=highestValue
		newHeight=block.height+block.size[1]
		#Updating new heights and new block for corresponding column
		for place in block.place:
			self.blockPos[place-1]=newHeight
			for b in self.blocks.values():
				if place in b.place and (b.height+b.size[1])==highestValue:
					b.blocksAbove.append(block.name)
			
		#Add block to table
		self.blocks[block.name]=block

	def removeBlock(self, blockName):
		block=self.blocks[blockName]
		blockHeight=block.size[1]
		for i in block.place:
			self.blockPos[i-1]-=blockHeight
		#Reevaluate blocks Above
		for b in self.blocks.values():
			if blockName in b.blocksAbove:
				b.blocksAbove.remove(blockName)
		self.blocks.pop(block.name)
		return block

	def displayTable(self):
		print(f"Block Position: {self.blockPos}")
		print(f"Blocks: {self.blocks}")

	def renderTable(self, blockToAnimate=None, blockChange=()):
		gameDisplay.fill(white)
		listofbaycontainers=[ display_width*i/self.size for i in range(self.size+1)]
		squareSide=listofbaycontainers[1]-listofbaycontainers[0]
		startHeight=display_height*0.9

		#Create Table Rectangle Display
		tableRect=Rect(0, startHeight, display_width, display_height)
		pygame.draw.rect(gameDisplay, black,tableRect)

		#Create Numbered Bays
		font = pygame.font.SysFont(None, 30)
		for i in range(self.size):
			textImg=font.render(str(i+1), True, white)
			gameDisplay.blit(textImg, (((listofbaycontainers[i+1]-listofbaycontainers[i])/2)+listofbaycontainers[i]-10, display_height*0.93))

		#Create blocks
		colorIndex=0
		colors=red, blue, green
		saveCorner=None
		for b in self.blocks.values():
			global block
			if blockToAnimate!=None:
				if b.name==blockToAnimate.name:
					block=Rect(squareSide*(b.place[0]-1)+blockChange[0], -squareSide*(b.height+b.size[1])+startHeight+blockChange[1], squareSide*b.size[0], squareSide*b.size[1])
					saveCorner=(squareSide*(b.place[0]-1)+blockChange[0], -squareSide*(b.height+b.size[1])+startHeight+blockChange[1])
				else:
					block=Rect(squareSide*(b.place[0]-1), -squareSide*(b.height+b.size[1])+startHeight, squareSide*b.size[0], squareSide*b.size[1])
			else:
				block=Rect(squareSide*(b.place[0]-1), -squareSide*(b.height+b.size[1])+startHeight, squareSide*b.size[0], squareSide*b.size[1])
			pygame.draw.rect(gameDisplay, b.color, block)
			pygame.draw.rect(gameDisplay, black, block, 2)
			nameImg=font.render(b.name, True, black)
			gameDisplay.blit(nameImg, (block.center[0]-10, block.center[1]-10))
			colorIndex+=1
		if blockToAnimate!=None:
			return saveCorner

	def newTree(self):
		self.goalTree=None
		goalTreeDict={}

	@dispatch(int)
	def searchBlocks(self, index):
		block=None
		for b in self.blocks.values():
			if index in b.place:
				if block==None:
					block=b
				else:
					if b.height>block.height:
						block=b
		return block

	@dispatch(str, str)
	def put_on(self, blockTopName, blockUnderName, parent=None):
		blockTop=self.blocks[blockTopName]
		if blockUnderName=='table':
			currentEmptyIndex=None
			for i in range(self.size):
				if self.blockPos[i]==0:
					currentEmptyIndex=i+1
					break
			if currentEmptyIndex!=None:
				if parent==None:
					self.put_on(self.blocks[blockTopName].place[0], currentEmptyIndex)
			else:
				pass
		else:
			blockUnder=self.blocks[blockUnderName]
			if self.goalTree==None:
				self.goalTree=GoalTree((blockTopName, blockUnderName))
				putOnNode=GoalTreeNode((blockTopName, blockUnderName), 'put on')
			else:
				putOnNode=self.goalTree.addNode((blockTopName, blockUnderName), 'put on', parent)
			#First see if both blockTop and blockUnder don't have blocks on top of them
			checkIntermediate=[ True for i in blockUnder.place if self.blockPos[i-1]==blockUnder.size[1]+blockUnder.height ]
			if blockTop.blocksAbove==[] and len(checkIntermediate)>=1:
				#Both blocks are on top directly move blockTop onto blockUnder
				#Check if surface for top block will be level
				levelConfigurationNum=None
				LevelIndexes={}
				PossibleLevelIndexes={}
				PossiblelevelConfigurationNum=None
				for underBlockPos in blockUnder.place:
					for topBlockPos in blockTop.place:
						difference=underBlockPos-topBlockPos
						newIndexes=[ i+difference for i in blockTop.place]
						largerThan=False
						for i in newIndexes:
							if i>self.size or i<=0:
								largerThan=True
						TopPlaceinNewIndex=False
						for i in blockTop.place:
							if i in newIndexes:
								TopPlaceinNewIndex=True
						if not largerThan:
							if LevelIndexes=={}:
								if not TopPlaceinNewIndex:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										LevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											LevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										blockFound=False
										for i in blockTop.place:
											pos=i+difference
											if self.searchBlocks(pos)==blockUnder:
												blockFound=True
										if blockFound:
											levelConfigurationNum=difference
								else:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										PossibleLevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											PossibleLevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										PossiblelevelConfigurationNum=difference
				if levelConfigurationNum==None and LevelIndexes=={}:
					LevelIndexes=PossibleLevelIndexes
					levelConfigurationNum=PossiblelevelConfigurationNum
				if levelConfigurationNum!=None:
					self.move(blockTop, blockUnder, putOnNode, levelConfigurationNum)
				else:
					#The area must first be leveled.
					self.level(LevelIndexes, blockTop, blockUnder, putOnNode)
			else:
				#If there are blocks on top of at least one of them
				if blockTop.blocksAbove!=[]:
					self.clearTop(blockTop, (blockTop, blockUnder), putOnNode, constraints=[blockUnder.place])
				elif blockUnder.blocksAbove!=[]:
					self.clearTop(blockUnder, (blockTop, blockUnder), putOnNode, constraints=[blockTop.place])
				self.put_on(blockTopName, blockUnderName, parent)

	@dispatch(str, str, object)
	def put_on(self, blockTopName, blockUnderName, parent=None):
		blockTop=self.blocks[blockTopName]
		if blockUnderName=='table':
			currentEmptyIndex=None
			for i in range(self.size):
				if self.blockPos[i]==0:
					currentEmptyIndex=i+1
					break
			if currentEmptyIndex!=None:
				if parent==None:
					self.put_on(self.blocks[blockTopName].place[0], currentEmptyIndex)
			else:
				pass
		else:
			blockUnder=self.blocks[blockUnderName]
			if self.goalTree==None:
				self.goalTree=GoalTree((blockTopName, blockUnderName))
				putOnNode=GoalTreeNode((blockTopName, blockUnderName), 'put on')
				
			else:
				putOnNode=self.goalTree.addNode((blockTopName, blockUnderName), 'put on', parent)
			#First see if both blockTop and blockUnder don't have blocks on top of them
			checkIntermediate=[ True for i in blockUnder.place if self.blockPos[i-1]==blockUnder.size[1]+blockUnder.height ]
			if blockTop.blocksAbove==[] and len(checkIntermediate)>=1:
				#Both blocks are on top directly move blockTop onto blockUnder
				#Check if surface for top block will be level
				levelConfigurationNum=None
				LevelIndexes={}
				PossibleLevelIndexes={}
				PossiblelevelConfigurationNum=None
				for underBlockPos in blockUnder.place:
					for topBlockPos in blockTop.place:
						difference=underBlockPos-topBlockPos
						newIndexes=[ i+difference for i in blockTop.place]
						largerThan=False
						for i in newIndexes:
							if i>self.size or i<=0:
								largerThan=True
						TopPlaceinNewIndex=False
						for i in blockTop.place:
							if i in newIndexes:
								TopPlaceinNewIndex=True
						if not largerThan:
							if LevelIndexes=={}:
								if not TopPlaceinNewIndex:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										LevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											LevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										blockFound=False
										for i in blockTop.place:
											pos=i+difference
											if self.searchBlocks(pos)==blockUnder:
												blockFound=True
										if blockFound:
											levelConfigurationNum=difference
								else:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										PossibleLevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											PossibleLevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										PossiblelevelConfigurationNum=difference
				if levelConfigurationNum==None and LevelIndexes=={}:
					LevelIndexes=PossibleLevelIndexes
					levelConfigurationNum=PossiblelevelConfigurationNum
				if levelConfigurationNum!=None:
					self.move(blockTop, blockUnder, putOnNode, levelConfigurationNum)
				else:
					#The area must first be leveled.
					self.level(LevelIndexes, blockTop, blockUnder, putOnNode)
			else:
				#If there are blocks on top of at
				if blockTop.blocksAbove!=[]:
					self.clearTop(blockTop, (blockTop, blockUnder), putOnNode, constraints=[blockUnder.place])
				elif blockUnder.blocksAbove!=[]:
					self.clearTop(blockUnder, (blockTop, blockUnder), putOnNode, constraints=[blockTop.place])
				self.put_on(blockTopName, blockUnderName, parent)

	@dispatch(int, int)
	def put_on(self, blockTopInd, blockUnderInd, parent=None):
		blockTop=self.searchBlocks(blockTopInd)
		if self.searchBlocks(blockUnderInd)==None:
			#This means that this is getting placed on the table
			if self.goalTree==None:
				self.goalTree=GoalTree((blockTop.name, 'table'))
				putOnNode=GoalTreeNode((blockTop.name, 'table'), 'put on')
			else:
				putOnNode=self.goalTree.addNode((self.searchBlocks(blockTopInd), 'table'), 'put on', parent)
			#Just worry about blockTop
			if blockTop.blocksAbove==[]:
				#Procede to check if space is available
				checkTable=True
				for i in range(blockTop.size[0]):
					ind=i+blockUnderInd-1
					if self.blockPos[ind]!=0:
						#There is not enough space on table location
						checkTable=False
				if checkTable:
					self.move(blockTop, blockUnderInd, putOnNode)
				else:
					#Make space on table to execute command
					pass
			else:
				#Cleartop of blockTop
				pass
		else:
			blockUnder=self.searchBlocks(blockUnderInd)
			putOnNode=self.goalTree.addNode((blockTop.name, blockUnder.name), 'put on', parent)
			#First see if both blockTop and blockUnder don't have blocks on top of them
			checkIntermediate=[ True for i in blockUnder.place if self.blockPos[i-1]==blockUnder.size[1]+blockUnder.height ]
			if blockTop.blocksAbove==[] and len(checkIntermediate)>=1:
				#Both blocks are on top directly move blockTop onto blockUnder
				#Check if surface for top block will be level
				levelConfigurationNum=None
				LevelIndexes={}
				PossibleLevelIndexes={}
				PossiblelevelConfigurationNum=None
				for underBlockPos in blockUnder.place:
					for topBlockPos in blockTop.place:
						difference=underBlockPos-topBlockPos
						newIndexes=[ i+difference for i in blockTop.place]
						largerThan=False
						for i in newIndexes:
							if i>self.size or i<=0:
								largerThan=True
						TopPlaceinNewIndex=False
						for i in blockTop.place:
							if i in newIndexes:
								TopPlaceinNewIndex=True
						if not largerThan:
							if LevelIndexes=={}:
								if not TopPlaceinNewIndex:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										LevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											LevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										levelConfigurationNum=difference
								else:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										PossibleLevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											PossibleLevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										PossiblelevelConfigurationNum=difference
				if levelConfigurationNum==None and LevelIndexes=={}:
					LevelIndexes=PossibleLevelIndexes
					levelConfigurationNum=PossiblelevelConfigurationNum
				if levelConfigurationNum!=None:
					self.move(blockTop, blockUnder, putOnNode, levelConfigurationNum)
				else:
					#The area must first be leveled.
					self.level(LevelIndexes, blockTop, blockUnder, putOnNode)
			else:
				#If there are blocks on top of at
				if blockTop.blocksAbove!=[]:
					self.clearTop(blockTop, (blockTop, blockUnder), putOnNode, constraints=[blockUnder.place])
				elif blockUnder.blocksAbove!=[]:
					self.clearTop(blockUnder, (blockTop, blockUnder), putOnNode, constraints=[blockTop.place])
				self.put_on(blockTopInd, blockUnderInd, parent)

	@dispatch(int, int, object)
	def put_on(self, blockTopInd, blockUnderInd, parent=None):
		blockTop=self.searchBlocks(blockTopInd)
		if self.searchBlocks(blockUnderInd)==None:
			#This means that this getting placed on the table
			if self.goalTree==None:
				self.goalTree=GoalTree((blockTop.name, 'table'))
				putOnNode=GoalTreeNode((blockTop.name, 'table'), 'put on')
			else:
				putOnNode=self.goalTree.addNode((self.searchBlocks(blockTopInd), 'table'), 'put on', parent)
			#Just worry about blockTop
			if blockTop.blocksAbove==[]:
				#Procede to check if space is available
				checkTable=True
				for i in range(blockTop.size[0]):
					ind=i+blockUnderInd-1
					if self.blockPos[ind]!=0:
						#There is not enough space on table location
						checkTable=False
				if checkTable:
					self.move(blockTop, blockUnderInd, putOnNode)
				else:
					#Make space on table to execute command
					pass
			else:
				#Cleartop of blockTop
				pass
		else:
			blockUnder=self.searchBlocks(blockUnderInd)
			putOnNode=self.goalTree.addNode((blockTop.name, blockUnder.name), 'put on', parent)
			#First see if both blockTop and blockUnder don't have blocks on top of them
			checkIntermediate=[ True for i in blockUnder.place if self.blockPos[i-1]==blockUnder.size[1]+blockUnder.height ]
			if blockTop.blocksAbove==[] and len(checkIntermediate)>=1:
				#Both blocks are on top directly move blockTop onto blockUnder
				#Check if surface for top block will be level
				levelConfigurationNum=None
				LevelIndexes={}
				PossibleLevelIndexes={}
				PossiblelevelConfigurationNum=None
				for underBlockPos in blockUnder.place:
					for topBlockPos in blockTop.place:
						difference=underBlockPos-topBlockPos
						newIndexes=[ i+difference for i in blockTop.place]
						largerThan=False
						for i in newIndexes:
							if i>self.size or i<=0:
								largerThan=True
						TopPlaceinNewIndex=False
						for i in blockTop.place:
							if i in newIndexes:
								TopPlaceinNewIndex=True
						if not largerThan:
							if LevelIndexes=={}:
								if not TopPlaceinNewIndex:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										LevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											LevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										levelConfigurationNum=difference
								else:
									levelity=True
									for i in newIndexes[:-1]:
										firstnumber=self.blockPos[i-1]
										secondnumber=self.blockPos[i]
										PossibleLevelIndexes[i]=firstnumber
										if firstnumber!=secondnumber:
											levelity=False
										if i==newIndexes[-2]:
											PossibleLevelIndexes[newIndexes[-1]]=secondnumber
									if levelity:
										PossiblelevelConfigurationNum=difference
				if levelConfigurationNum==None and LevelIndexes=={}:
					LevelIndexes=PossibleLevelIndexes
					levelConfigurationNum=PossiblelevelConfigurationNum
				if levelConfigurationNum!=None:
					self.move(blockTop, blockUnder, putOnNode, levelConfigurationNum)
				else:
					#The area must first be leveled.
					self.level(LevelIndexes, blockTop, blockUnder, putOnNode)
			else:
				#If there are blocks on top of at
				if blockTop.blocksAbove!=[]:
					self.clearTop(blockTop, (blockTop, blockUnder), putOnNode, constraints=[blockUnder.place])
				elif blockUnder.blocksAbove!=[]:
					self.clearTop(blockUnder, (blockTop, blockUnder), putOnNode,constraints=[blockTop.place])
				self.put_on(blockTopInd, blockUnderInd, parent)

	@dispatch(Block, Block, GoalTreeNode, int)
	def move(self, blockTop, blockUnder, parentNode, specificInd):
		#Note if specificInd is provided this should be the way the indexes should match up.
		self.animateMove(blockTop, blockTop.place[0]+specificInd)
		oldblock=table.removeBlock(blockTop.name)
		table.addBlock([oldblock.size, int(oldblock.place[0]+specificInd), oldblock.name, oldblock.color])
		moveNode=self.goalTree.addNode((blockTop.name, blockUnder.name), 'move', parentNode)

	@dispatch(Block, int, GoalTreeNode)
	def move(self, blockTop, blockUnderInd, parentNode):
		#Note if specificInd is provided this should be the way the indexes should match up.
		if self.searchBlocks(blockUnderInd)==None:
			moveNode=self.goalTree.addNode((blockTop.name, 'table'), 'move', parentNode)
		else:
			moveNode=self.goalTree.addNode((blockTop.name, self.searchBlocks(blockUnderInd).name), 'move', parentNode)
		self.animateMove(blockTop, blockUnderInd)
		oldblock=table.removeBlock(blockTop.name)
		table.addBlock([oldblock.size, blockUnderInd, oldblock.name, oldblock.color])

	def animateMove(self, blockTop, blockEndPos):
		gameDisplay.fill(white)
		corner=(200,200)
		x_increment=0
		y_increment=0
		incrementSpeed=5
		while corner[1]>100:
			gameDisplay.fill(white)
			corner=self.renderTable(blockToAnimate=blockTop, blockChange=(0, y_increment))
			y_increment-=incrementSpeed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			pygame.display.update()
		for i in range(25):
			gameDisplay.fill(white)
			corner=self.renderTable(blockToAnimate=blockTop, blockChange=(0, y_increment))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			pygame.display.update()
		listofbaycontainers=[ display_width*i/self.size for i in range(self.size+1)]
		squareSide=listofbaycontainers[1]-listofbaycontainers[0]
		startHeight=display_height*0.9
		expectedCorner=(squareSide*(blockEndPos-1), -squareSide*(self.blockPos[blockEndPos-1]+blockTop.size[1])+startHeight)
		if blockTop.place[0]<blockEndPos:
			#Go right
			while corner[0]<expectedCorner[0]:
				gameDisplay.fill(white)
				corner=self.renderTable(blockToAnimate=blockTop, blockChange=(x_increment, y_increment))
				x_increment+=incrementSpeed
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
				pygame.display.update()
			x_increment-=incrementSpeed
		else:
			#Go left
			while corner[0]>expectedCorner[0]:
				gameDisplay.fill(white)
				corner=self.renderTable(blockToAnimate=blockTop, blockChange=(x_increment, y_increment))
				x_increment-=incrementSpeed
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
				pygame.display.update()
			x_increment+=incrementSpeed
		for i in range(25):
			gameDisplay.fill(white)
			corner=self.renderTable(blockToAnimate=blockTop, blockChange=(x_increment, y_increment))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			pygame.display.update()
		#Move down
		while corner[1]<expectedCorner[1]:
			gameDisplay.fill(white)
			corner=self.renderTable(blockToAnimate=blockTop, blockChange=(x_increment, y_increment))
			y_increment+=incrementSpeed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			pygame.display.update()

	def getBlock(self, size, constraints=[],onTop=True):
		if onTop:
			for block in self.blocks.values():
				if block.height+block.size[1]==self.blockPos[block.place[0]-1]:
					if block.size==size and block not in constraints:
						return block
			return None
		else:
			block=None
			difference=None
			for b in self.blocks.values():
				if block==None:
					block=b
					difference=self.blockPos[block.place[0]]-block.height-block.size[1]
				else:
					if difference>self.blockPos[b.place[0]]-b.height-b.size[1]:
						block=b
						difference=self.blockPos[block.place[0]]-block.height-block.size[1]
			return block

	def checkLevel(self, blockTop, blockUnder):
		#Check if surface for top block will be level
		levelConfigurationNum=None
		LevelIndexes={}
		PossibleLevelIndexes={}
		PossiblelevelConfigurationNum=None
		for underBlockPos in blockUnder.place:
			for topBlockPos in blockTop.place:
				difference=underBlockPos-topBlockPos
				newIndexes=[ i+difference for i in blockTop.place]
				largerThan=False
				for i in newIndexes:
					if i>self.size or i<=0:
						largerThan=True
				TopPlaceinNewIndex=False
				for i in blockTop.place:
					if i in newIndexes:
						TopPlaceinNewIndex=True
				if not largerThan:
					if LevelIndexes=={}:
						if not TopPlaceinNewIndex:
							levelity=True
							for i in newIndexes[:-1]:
								firstnumber=self.blockPos[i-1]
								secondnumber=self.blockPos[i]
								LevelIndexes[i]=firstnumber
								if firstnumber!=secondnumber:
									levelity=False
								if i==newIndexes[-2]:
									LevelIndexes[newIndexes[-1]]=secondnumber
							if levelity:
								levelConfigurationNum=difference
						else:
							levelity=True
							for i in newIndexes[:-1]:
								firstnumber=self.blockPos[i-1]
								secondnumber=self.blockPos[i]
								PossibleLevelIndexes[i]=firstnumber
								if firstnumber!=secondnumber:
									levelity=False
								if i==newIndexes[-2]:
									PossibleLevelIndexes[newIndexes[-1]]=secondnumber
							if levelity:
								PossiblelevelConfigurationNum=difference
		if levelConfigurationNum==None and LevelIndexes=={}:
			LevelIndexes=PossibleLevelIndexes
			levelConfigurationNum=PossiblelevelConfigurationNum
		if levelConfigurationNum!=None:
			return None
		else:
			return LevelIndexes

	def clearTop(self, blocktoClearTopOf, task, parentNode, constraints=[]):
		if blocktoClearTopOf.blocksAbove!=[]:
			clearTopNode=self.goalTree.addNode(blocktoClearTopOf.name, 'clear top', parentNode)
			for blockName in blocktoClearTopOf.blocksAbove:
				block=self.blocks[blockName]
				if block.blocksAbove==[]:
					self.getridOf(block, clearTopNode, constraints)
				else:
					self.clearTop(block, task, clearTopNode, constraints)
		else:
			sys.exit('Something is wrong with implementation of clear top method.')

	def getridOf(self, blockToMove, parentNode, constraints=[]):
		value=None
		newValue=None
		posList=[]
		for i in range(len(self.blockPos)-1):
			value=self.blockPos[i]
			newValue=self.blockPos[i+1]
			#Passive distrubution technique
			if newValue>3:
				continue
			if blockToMove.size[0]>1:
				if value==newValue and value<=3:
					if i+1 not in posList:
						posList.append(i+1)
					if i+2 not in posList:
						posList.append(i+2)
				else:
					posList=[]
			else:
				if value<=3:
					posList.append(i+1)
			if len(posList)>=blockToMove.size[0]:
				check=True
				for i in posList:
					for places in constraints:
						if i in places:
							check=False
				if check:
					if self.searchBlocks(posList[0])==None:
						ridNode=self.goalTree.addNode((blockToMove.name, 'table'), 'get rid', parentNode)
					else:
						ridNode=self.goalTree.addNode((blockToMove.name, self.searchBlocks(posList[0]).name), 'get rid', parentNode)
					self.move(blockToMove, posList[0], ridNode)
					break

	def level(self, LevelIndexes, blockTop, blockUnder, parentNode):
		#First find max
		contains=[True for i in blockTop.place if i in LevelIndexes]
		if True in contains:
			#Move blockTop by getting rid of
			pass
		levelNode=self.goalTree.addNode((blockTop.name, blockUnder.name), 'level', parentNode)
		if blockTop.size[0]>blockUnder.size[0]:
			#This means that blockTop.size[0]=2 and blockUnder.size[0]=1
			blockUnderIndex=blockUnder.place[0]
			maxVal=0
			maxValInd=None
			minVal=None
			minValInd=None
			for k in LevelIndexes.keys():
				if LevelIndexes[k]>maxVal:
					maxVal=LevelIndexes[k]
					maxValInd=k
			for k in LevelIndexes.keys():
				if minVal==None:
					minValInd=k
					minVal=LevelIndexes[k]
				else:
					if LevelIndexes[k]<minVal:
						minVal=LevelIndexes[k]
						minValInd=k
			difference=maxVal-minVal
			if maxValInd==blockUnderIndex:
				#Move another block from elsewhere to fill space
				difference=maxVal-minVal
				if difference>2:
					addedVal=2
					levelingBlock=self.getBlock([1, 2], [blockTop, blockUnder])
					if levelingBlock==None:
						levelingBlock=self.getBlock([1, 1], [blockTop, blockUnder])
						addedVal=1
					self.move(levelingBlock, minValInd, levelNode)
					newLevelIndex=LevelIndexes
					newLevelIndex[minValInd]+=addedVal
					if newLevelIndex!=None:
						self.level(newLevelIndex, blockTop, blockUnder, parentNode)
				else:
					levelingBlock=self.getBlock([1, difference], [blockTop, blockUnder])
					if levelingBlock==None or minValInd-1 in levelingBlock.place:
						levelingBlock=self.getBlock([1, 1], [blockTop, blockUnder])
					if levelingBlock==None or minValInd-1 in levelingBlock.place:
						levelingBlock=self.getBlock([2, difference], [blockTop, blockUnder])
					if levelingBlock==None or minValInd-1 in levelingBlock.place:
						sys.exit('No Open Leveling Block exists')
					self.move(levelingBlock, minValInd, levelNode)
					self.put_on(blockTop.name, blockUnder.name)
			elif minValInd==blockUnderIndex:
				ridblock=self.searchBlocks(maxValInd)
				self.getridOf(ridblock, levelNode,[blockTop.place, blockUnder.place])
				newLevelIndex=self.checkLevel(blockTop, blockUnder)
				self.level(newLevelIndex, blockTop, blockUnder, parentNode)
		else:
			sys.exit('Something must have gone wrong with logic.')
#Creating Table with blocks
Block.resetColorIndex()
table=Table(10)
table.addBlock([[2,2], 3, "b1"])
table.addBlock([[1,1], 2, "b2"])
table.addBlock([[1,1], 2, "b3"])
table.addBlock([[1,1], 5, "b4"])
table.addBlock([[1,2], 6, "b5"])
table.addBlock([[2,1], 7, "b6"])
table.addBlock([[1,1], 9, "b7"])
table.addBlock([[1,2], 10, "b8"])
#Display Driver Code	
text=""
while True:
	clock.tick(FPS)
	gameDisplay.fill(white)
	#Create display of current state of table
	table.renderTable()
	textboxInput(text)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_BACKSPACE:
				if len(text)>0:
					text = text[:-1]
			elif event.key == K_RETURN:
				text=text.lower()
				#Do logic to check questions
				if '?' in text or 'why' in text or 'how' in text:
					print("\nComputer: ")
					#This is a question
					if 'why' in text:
						#Go one layer up in tree or get immediate parent
						if goalTreeDict=={}:
							print("I can't answer questions about actions that I haven't done!")
						if 'move' in text or 'put' in text or 'level' in text or 'rid' in text or 'clear' in text:
							textList=text.split(' ')
							if 'clear' in text:
								if '?' in text:
									topBlockName=textList[-1][:-1]
								else:
									topBlockName=textList[-1]
							else:
								if 'to' in text:
									topBlockName=textList[textList.index('to')-1]
									if '?' in text:
										underBlockName=textList[textList.index('to')+1][:-1]
									else:
										underBlockName=textList[textList.index('to')+1]
								elif 'on' in text:
									topBlockName=textList[textList.index('on')-1]
									if '?' in text:
										underBlockName=textList[textList.index('on')+1][:-1]
									else:
										underBlockName=textList[textList.index('on')+1]
							try:
								if 'move' in text:
									moveNode=goalTreeDict['move '+topBlockName+'-->'+underBlockName]
								elif 'put' in text:
									moveNode=goalTreeDict['put on '+topBlockName+'-->'+underBlockName]
								elif 'level' in text:
									moveNode=goalTreeDict['level '+topBlockName+'-->'+underBlockName]
								elif 'clear' in text:
									moveNode=goalTreeDict['clear top '+topBlockName+'-->'+'None']
								else:
									moveNode=goalTreeDict['get rid '+topBlockName+'-->'+underBlockName]
								if moveNode.parent==None:
									print('Because you told me to.')
								else:
									print('To '+moveNode.parent.replace('-->', ' to '))
							except KeyError:
								print("Did I do that?")
							except NameError:
								print("Sorry I didn't understand your question.")
					elif 'how' in text and 'show' not in text:
						if goalTreeDict=={}:
							print("I can't answer questions about actions that I haven't done!")
						else:
							if 'put' in text or 'level' in text or 'rid' in text or 'clear' in text:
								textList=text.split(' ')
								if 'clear' in text:
									if '?' in text:
										topBlockName=textList[-1][:-1]
									else:
										topBlockName=textList[-1]
								else:
									if 'to' in text:
										topBlockName=textList[textList.index('to')-1]
										if '?' in text:
											underBlockName=textList[textList.index('to')+1][:-1]
										else:
											underBlockName=textList[textList.index('to')+1]
									elif 'on' in text:
										topBlockName=textList[textList.index('on')-1]
										if '?' in text:
											underBlockName=textList[textList.index('on')+1][:-1]
										else:
											underBlockName=textList[textList.index('on')+1]
								try:
									if 'move' in text:
										moveNode=goalTreeDict['move '+topBlockName+'-->'+underBlockName]
									elif 'put' in text:
										moveNode=goalTreeDict['put on '+topBlockName+'-->'+underBlockName]
									elif 'clear' in text:
										moveNode=goalTreeDict['clear top '+topBlockName+'-->'+'None']
									elif 'level' in text:
										moveNode=goalTreeDict['level '+topBlockName+'-->'+underBlockName]
									else:
										moveNode=goalTreeDict['get rid '+topBlockName+'-->'+underBlockName]
									if moveNode.children==[]:
										print("I should know, but I don't. Something is wrong with me!!!")
									else:
										print('By:')
										for i in moveNode.children:
											if 'clear' in i:
												print('--->'+i.replace('-->None',''))
											else:
												print('--->'+i.replace('-->', ' to '))
								except KeyError:
									print("Did I do that?")
								except NameError:
									print("Sorry I didn't understand your question.")
							elif 'move' in text:
								print("It was a basic task of moving.")
							else:
								print("Sorry I didn't understand your question.")
					else:
						print("Sorry I didn't understand your question.")
				elif '-->' in text:
					table.newTree()
					goalTreeDict={}
					blocks=text.split('-->')
					blockTopName=blocks[0]
					blockUnderName=blocks[1]
					if blockTopName.isdigit() and blockUnderName.isdigit():
						blockTopName=int(blocks[0])
						blockUnderName=int(blocks[1])
					if blockTopName in table.blocks.keys() and blockUnderName in table.blocks.keys():
						table.put_on(blockTopName, blockUnderName)
					else:
						print("I couldn't understand your command. Please check your spelling.")
				elif 'reset' in text:
					keys=[i for i in table.blocks.keys()]
					for blockName in keys:
						table.removeBlock(blockName)
					Block.resetColorIndex()
					table.addBlock([[2,2], 3, "b1"])
					table.addBlock([[1,1], 2, "b2"])
					table.addBlock([[1,1], 2, "b3"])
					table.addBlock([[1,1], 5, "b4"])
					table.addBlock([[1,2], 6, "b5"])
					table.addBlock([[2,1], 7, "b6"])
					table.addBlock([[1,1], 9, "b7"])
					table.addBlock([[1,2], 10, "b8"])
				else:
					print("\nComputer: ")
					print("Sorry I couldn't quite get your command.")
				#This should be after all logic
				text=""
			else:
				text += event.unicode
				font = pygame.font.SysFont(None, 30)
				img = font.render(text, True, black)
				rect = img.get_rect()
				rect.topleft = (20, 20)
				rect.size=img.get_size()
				cursor = Rect(rect.topright, (3, rect.height))
				cursor.topleft = rect.topright
	pygame.display.update()
