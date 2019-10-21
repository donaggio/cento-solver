'''
Solves a "Cento" board of arbitrary dimensions (from 5x5 to 10x10) using a brute-force algorithm

(c) 2019 Luca Donaggio <donaggio at gmail dot com>
'''
import argparse

class Coord:
	def __init__(self, col, row):
		self.x = col
		self.y = row

class Move:
	def __init__(self, col, row, num):
		self.coord = Coord(col, row)
		self.num = num
		self.nextMoves = {'N': '', 'NE': '', 'E': '', 'SE': '', 'S': '', 'SW': '', 'W': '', 'NW': ''}
	
class Game:
	def __init__(self, dim):
		self.dim = dim
		self.board = [[None for x in range(self.dim)] for y in range(self.dim)]
		self.currMove = None
		self.moves = []
		self.step = 0
	
	def _dirToCoord(self, dir):
		if dir == 'N':
			return Coord(self.currMove.coord.x, self.currMove.coord.y - 3)
		elif dir == 'NE':
			return Coord(self.currMove.coord.x + 2, self.currMove.coord.y - 2)
		elif dir == 'E':
			return Coord(self.currMove.coord.x + 3, self.currMove.coord.y)
		elif dir == 'SE':
			return Coord(self.currMove.coord.x + 2, self.currMove.coord.y + 2)
		elif dir == 'S':
			return Coord(self.currMove.coord.x, self.currMove.coord.y + 3)
		elif dir == 'SW':
			return Coord(self.currMove.coord.x - 2, self.currMove.coord.y + 2)
		elif dir == 'W':
			return Coord(self.currMove.coord.x - 3, self.currMove.coord.y)
		elif dir == 'NW':
			return Coord(self.currMove.coord.x - 2, self.currMove.coord.y - 2)

	def _evalNextMove(self, dir):
		nextCoord = self._dirToCoord(dir)
		if nextCoord.x in range(self.dim) and nextCoord.y in range(self.dim):
			if self.board[nextCoord.y][nextCoord.x] is None:
				return 'V'
			else:
				return 'X'
		else:
			return 'I'

	def _nextMove(self):
		# Evaluate all possible moves
		for d in self.currMove.nextMoves:
			if not self.currMove.nextMoves[d]:
				self.currMove.nextMoves[d] = self._evalNextMove(d)
		# Choose next move
		nextDir = ''
		for di in self.currMove.nextMoves.items():
			if di[1] == 'V':
				nextDir = di[0]
				break
		if nextDir:
			self.currMove.nextMoves[nextDir] = 'P'
			nextCoord = self._dirToCoord(nextDir)
			return Move(nextCoord.x, nextCoord.y, self.currMove.num + 1)
		else:
			return None

	def _printProgress(self):
		print ('\rStep ' + str(self.step) + ': [{0:<' + str(self.dim ** 2) + '}]').format('#' * self.currMove.num),

	def solve(self):
		# Start at top-left corner
		move = Move(0, 0, 1)
		while move is not None:
			# Do move
			self.moves.append(move)
			self.currMove = move
			self.board[move.coord.y][move.coord.x] = move.num
			# Print progress indicator
			self._printProgress()
			# Have we finished?
			if move.num == self.dim ** 2:
				return
			# No, choose next move
			nextMove = self._nextMove()
			# Are there no more moves?
			while nextMove is None:
				# Undo current move
				self.board[self.currMove.coord.y][self.currMove.coord.x] = None
				self.moves.pop()
				# Is there a previous move?
				if len(self.moves) > 0:
					# Yes, make that the current move
					self.currMove = self.moves[-1]
					# Print progress indicator
					self._printProgress()
					# Mark the former move as 'failed' so to not go there again
					for d in self.currMove.nextMoves:
						if self.currMove.nextMoves[d] == 'P':
							self.currMove.nextMoves[d] = 'F'
							break
					# Choose next m ve
					nextMove = self._nextMove()
				else:
					# No, restart from next position on the board
					self.currMove = None
					self.step += 1
					if self.step < self.dim ** 2:
						nextMove = Move(self.step // self.dim, self.step % self.dim, 1)
					else:
						print
						return
			move = nextMove
		return
	
	def printBoard(self):
		maxNumWidth = len(str(self.dim ** 2))
		cellWidth = maxNumWidth + 2
		rowDiv = '+' + ('-' * ((cellWidth + 1 ) * self.dim - 1)) + '+'

		for row in range(self.dim):
			print rowDiv
			print '|',
			for col in range(self.dim):
				if self.board[row][col] is not None:
					print ('{n:<' + str(maxNumWidth) + '} |').format(n = self.board[row][col]),
				else:
					print '-' * maxNumWidth + ' |',
			print
		print rowDiv

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Solves a "Cento" board of given dimensions.')
	parser.add_argument("-d", "--dim", type = int, choices = [5, 6, 7, 8, 9, 10], default = 5, help = 'board dimension')
	args = parser.parse_args()

	print '\n"Cento" solver (c) 2019 Luca Donaggio <donaggio at gmail dot com>\n\nSolving a {dim}x{dim} board:\n'.format(dim = args.dim)
	game = Game(args.dim)
	game.solve()
	print '\n'
	game.printBoard()
	print
