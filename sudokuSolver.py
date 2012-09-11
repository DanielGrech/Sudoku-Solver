#!/usr/bin/python
import sys
import random

BRUTE_FORCE = True

class Color:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'

	@staticmethod
	def disable():
		Color.BLUE = ''
		Color.GREEN = ''
		Color.WARNING = ''
		Color.FAIL = ''
		Color.END = ''

class Cell:
	""" Represents a single cell on a sudoku board """
	EMPTY_CELL_VALUE = -1
	def __init__(self, value = EMPTY_CELL_VALUE):
		self.value = value
		if value == Cell.EMPTY_CELL_VALUE:
			self.possibleValues = [1,2,3,4,5,6,7,8,9]
			self.computed = True
		else:
			self.possibleValues = []
			self.computed = False

	def __repr__(self):
		#return str(self.possibleValues)
		if self.value == Cell.EMPTY_CELL_VALUE:
			return Color.WARNING + "_"+ Color.END
		else:
			if self.computed:
				return Color.GREEN + str(self.value) + Color.END
			else:
				return Color.BLUE + str(self.value) + Color.END

	def __str__(self):
		return self.__repr__()

	def remove_possible(self, value):
		if type(value) is list or type(value) is set:
			for val in value:
				if val in self.possibleValues:
					self.possibleValues.remove(val)	
		else :
			if value in self.possibleValues:
				self.possibleValues.remove(value)

		if len(self.possibleValues) == 1:
			self.value = self.possibleValues[0]
			self.possibleValues = []

def getBoard(filename):
	board = []
	file = open(filename)
	for line in file:
		line = line.strip("\n")
		cells = line.split(",")
		
		row = []	
		for val in cells:
			if val.isdigit():
				row.append(Cell(int(val)))
			else:
				row.append(Cell())

		board.append(row)

	return board

def printBoard(board, stream = sys.stdout):
	for i in range(0, len(board)): #
		row = board[i]

		if i > 0 and i % 3 == 0:
			print ''

		first = True
		toPrint = ""
		for j in range(0, len(row)):
			if j > 0 and j % 3 == 0:
				toPrint += '\t'
			if first:
				first = False
			else:
				toPrint += " " 
			
			toPrint += str(row[j])

		print >> stream, toPrint


def getColumn(board, colNum):
	return [row[colNum] for row in board]

def removeByRow(board):
	for row in board:
		appeared = []
		for cell in row:
			if cell.value is not Cell.EMPTY_CELL_VALUE:
				appeared.append(cell.value)
		for cell in row:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				cell.remove_possible(appeared)		

def removeByColumn(board):
	for i in range(0, len(board)):
		columnValues = getColumn(board, i)
	 	appeared = []
	 	for cell in columnValues:
			if cell.value is not Cell.EMPTY_CELL_VALUE:
				appeared.append(cell.value)
		for cell in columnValues:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				cell.remove_possible(appeared)	

def removeByBox(board):
	boxes = getBoxes(board)
	

	for key in boxes:
		box = boxes[key]
		appeared = set()
		for row in box:
			for cell in row:
				if cell.value is not Cell.EMPTY_CELL_VALUE:
					appeared.add(cell.value)

		for row in box:
			for cell in row:
				cell.remove_possible(appeared)

def getBoxes(board):
	boxes = {}
	for i in range(0, len(board)):
		first_three_cols = board[i][:3]
		second_three_cols = board[i][3:6]
		third_three_cols = board[i][6:]

		if i < 3:
			if not 0 in boxes:
				boxes[0] = []
			boxes[0].append(first_three_cols)

			if not 1 in boxes:
				boxes[1] = []
			boxes[1].append(second_three_cols)

			if not 2 in boxes:
				boxes[2] = []
			boxes[2].append(third_three_cols)
			pass
		elif i < 6:
			if not 3 in boxes:
				boxes[3] = []
			boxes[3].append(first_three_cols)

			if not 4 in boxes:
				boxes[4] = []
			boxes[4].append(second_three_cols)

			if not 5 in boxes:
				boxes[5] = []
			boxes[5].append(third_three_cols)
			pass
		else:
			if not 6 in boxes:
				boxes[6] = []
			boxes[6].append(first_three_cols)

			if not 7 in boxes:
				boxes[7] = []
			boxes[7].append(second_three_cols)

			if not 8 in boxes:
				boxes[8] = []
			boxes[8].append(third_three_cols)
			pass
	return boxes

def remove_impossible_values(board):
	#First, we remove any values which we know arent possible

	#..by row
	removeByRow(board)

	#..then by column
	removeByColumn(board)

	#..and finally in the 3x3 box
	removeByBox(board)

def get_missing_cell_count(board):
	count = 0
	for row in board:
		for cell in row:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				count = count + 1

	return count

def is_finished(board):
	for row in board:
		row_numbers = [x for x in range(1,10)]
		for cell in row:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				return False
			elif cell.value in row_numbers:
				row_numbers.remove(cell.value)
		if len(row_numbers) is not 0:
			return False


	for i in range(0, len(board)):
		columnValues = getColumn(board, i)
		column_numbers = [x for x in range(1,10)]
		for cell in columnValues:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				return False
			elif cell.value in column_numbers:
				column_numbers.remove(cell.value)
		if len(column_numbers) is not 0:
			return False

	return True

def infer_row_values(board):
	for row in board:
		value_map = {} 
		for cell in row:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				possible_cells = None
				for pv in cell.possibleValues:
					if pv in value_map:
						possible_cells = value_map[pv]
					else:
						possible_cells = []

					possible_cells.append(cell)
					value_map[pv] = possible_cells
		for v in value_map:
			cell_list = value_map[v]
			if len(cell_list) == 1:
				cell_list[0].value = v
				cell_list[0].possibleValues = []

def infer_column_values(board):
	for i in range(0, len(board)):
		column = getColumn(board, i)
		value_map = {} 
		for cell in column:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				possible_cells = None
				for pv in cell.possibleValues:
					if pv in value_map:
						possible_cells = value_map[pv]
					else:
						possible_cells = []

					possible_cells.append(cell)
					value_map[pv] = possible_cells
		for v in value_map:
			cell_list = value_map[v]
			if len(cell_list) == 1:
				cell_list[0].value = v
				cell_list[0].possibleValues = []

def infer_box_values(board):
	boxes = getBoxes(board)
	for box_num in boxes:
		box = boxes[box_num]
		value_map = {} 
		for row in box:
			for cell in row:
				if cell.value == Cell.EMPTY_CELL_VALUE:
					possible_cells = None	
					for pv in cell.possibleValues:
						if pv in value_map:
							possible_cells = value_map[pv]
						else:
							possible_cells = []
						possible_cells.append(cell)
						value_map[pv] = possible_cells	
		for v in value_map:
			cell_list = value_map[v]
			if len(cell_list) == 1:
				cell_list[0].value = v
				cell_list[0].possibleValues = []

def infer_naked_pairs_row(board):
	for row in board:
		missing = []
		for cell in row:
			if cell.value == Cell.EMPTY_CELL_VALUE:
				missing.append(cell)
		if len(missing) == 2:
			pass

def infer_naked_pairs_box(board):
	boxes = getBoxes(board)
	for box_num in boxes:
		box = boxes[box_num]
		missing = []
		for row in box:
			for cell in row:
				if cell.value == Cell.EMPTY_CELL_VALUE:
					missing.append(cell)
		if len(missing) == 2:
			pass

def solveRecursive(board, empty_cells = []):
	if len(empty_cells) == 0:
		for row in board:
			for cell in row:
				if cell.value == Cell.EMPTY_CELL_VALUE:
					for val in cell.possibleValues:
						cell.value = val
						if is_finished(board):
							return True
						else:
							return solveRecursive(board)

	# 	#Start off with any possible value for each cell
	# 	for c in empty_cells:
	# 		c.value = c.possibleValues[0]

	# if len(empty_cells) == 0:
	# 	return True

	# c = empty_cells.pop()


	# for val in c.possibleValues:
	# 	c.value = val
	# 	if is_finished(board):
	# 		return True
	# 	else:
	# 		return solveRecursive(board, empty_cells)


def solveBruteForce(board):
	empty_cells = []
	if len(empty_cells) == 0:
		for row in board:
			for cell in row:
				if cell.value == Cell.EMPTY_CELL_VALUE:
					empty_cells.append(cell)


	#Start off with any possible value for each cell
	for c in empty_cells:
		c.value = c.possibleValues[0]



	for cell in empty_cells:
		for cell2 in empty_cells:
			if cell == cell2:
				continue
			for val in cell2.possibleValues:
				print "Trying", val
				cell2.value = val
				if is_finished(board):
					return True

		for val in cell.possibleValues:
			cell.value = val
			if is_finished(board):
				return True

def repeat_until_no_effect(board, func):
	missing_cell_count = get_missing_cell_count(board)
	while True:
		func(board)

		new_missing_cell_count = get_missing_cell_count(board)
		if missing_cell_count == new_missing_cell_count:
			break
		else:
			missing_cell_count = new_missing_cell_count	

def solve(board):
	repeat_until_no_effect(board, remove_impossible_values)
	if is_finished(board):
		return
	repeat_until_no_effect(board, infer_row_values)
	repeat_until_no_effect(board, remove_impossible_values)
	if is_finished(board):
		return

	repeat_until_no_effect(board, infer_column_values)
	repeat_until_no_effect(board, remove_impossible_values)
	if is_finished(board):
		return

	repeat_until_no_effect(board, infer_box_values)
	repeat_until_no_effect(board, infer_naked_pairs_box)
	repeat_until_no_effect(board, remove_impossible_values)

#--------- Main ---------
if len(sys.argv) < 2:
	raise Exception("Must pass input name from CLI")

board = getBoard(sys.argv[1])

# Iterate until we cant make any more improvements
repeat_until_no_effect(board, solve)

printBoard(board)

if not is_finished(board):
	solveRecursive(board)



if is_finished(board):
	print Color.GREEN + "Winner!" + Color.END
else:
	print Color.FAIL + "Loser!" + Color.END


