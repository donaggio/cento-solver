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
	def __init__(self, rows, cols):
		self.rows, self.cols = rows, cols
		self.matrix = [[None for x in range(self.cols)] for y in range(self.rows)]
		self.currMove = None
		self.moves = []
	
	def _dirToCoord(self, dir):
		if dir == 'N':
			return Coord(self.currMove.coord.x, self.currMove.coord.y - 2)
		elif dir == 'NE':
			return Coord(self.currMove.coord.x + 1, self.currMove.coord.y - 1)
		elif dir == 'E':
			return Coord(self.currMove.coord.x + 2, self.currMove.coord.y)
		elif dir == 'SE':
			return Coord(self.currMove.coord.x + 1, self.currMove.coord.y + 1)
		elif dir == 'S':
			return Coord(self.currMove.coord.x, self.currMove.coord.y + 2)
		elif dir == 'SW':
			return Coord(self.currMove.coord.x - 1, self.currMove.coord.y + 1)
		elif dir == 'W':
			return Coord(self.currMove.coord.x - 2, self.currMove.coord.y)
		elif dir == 'NW':
			return Coord(self.currMove.coord.x - 1, self.currMove.coord.y - 1)

	def _evalNextMove(self, dir):
		nextCoord = self._dirToCoord(dir)
		if nextCoord.x in range(self.cols) or nextCoord.y in range(self.rows):
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
			nextCoord = self._dirToCoord(nextDir)
			return Move(nextCoord.x, nextCoord.y, self.currMove.num + 1)
		else:
			return None

	def solve(self):
		nextMove = Move(0, 0, 1)
		while nextMove is not None:
			self.moves.append(nextMove)
			self.currMove = nextMove
			self.matrix[nextMove.coord.x][nextMove.coord.y] = nextMove.num
			nextMove = self._nextMove()
		
		# DEBUG
		print self.matrix

game = Game(5, 5)
game.solve()
