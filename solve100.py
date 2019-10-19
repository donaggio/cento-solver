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
		self.matrix = [[None for x in range(self.dim)] for y in range(self.dim)]
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
			if self.matrix[nextCoord.x][nextCoord.y] is None:
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

	def solve(self, move):
		while move is not None:
			self.moves.append(move)
			self.currMove = move
			self.matrix[move.coord.x][move.coord.y] = move.num
			# DEBUG
			# print str(self.currMove.num),
			nextMove = self._nextMove()
			while nextMove is None:
				self.matrix[self.currMove.coord.x][self.currMove.coord.y] = None
				self.moves.pop()
				if len(self.moves) > 0:
					self.currMove = self.moves[-1]
					# DEBUG
					# print str(self.currMove.num),
					for d in self.currMove.nextMoves:
						if self.currMove.nextMoves[d] == 'P':
							self.currMove.nextMoves[d] = 'F'
							break
					nextMove = self._nextMove()
				else:
					self.step += 1
					if self.step < self.dim ** 2:
						nextMove = Move(self.step // self.dim, self.step % self.dim, 1)
						# DEBUG
						print
						print 'Step ' + str(self.step) + ' (' + str(nextMove.coord.x) + ',' + str(nextMove.coord.y) + '):'
						print
					else:
						print
						return
			move = nextMove
	
	def printBoard(self):
		for row in range(self.dim):
			print '-----' * self.dim
			for col in range(self.dim):
				if self.matrix[row][col] is not None:
					print ' {n:<3}'.format(n = self.matrix[row][col]),
				else:
					print ' ---',
			print
		print '-----' * self.dim

game = Game(5)
game.solve(Move(0, 0, 1))
game.printBoard()
