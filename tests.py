DIRECTIONS = {"N":(-1,0),"NE":(-1,1),"E":(0,1),"SE":(1,1),
              "S":(1,0),"SW":(1,-1),"W":(0,-1),"NW":(-1,-1)}

class Board:
    def __init__(self, B, D):
        self.B = B
        self.D = D
    def __hash__(self):
        return hash(self.B)
    def __eq__(self, other):
        return self.B == other.B
    def is_solved(self):
        nonempty = False
        for p in self:
            if nonempty:
                return False
            nonempty=True
        return nonempty
    def is_legal_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        before = (1, 1, 0)
        if orientation == "reverse":
            before = (0, 0, 1)
        for i in range(3):
            if self[r + i*dr, c + i*dc] != before[i]:
                return False
        return True
    def all_legal_moves(self, orientation = "forward"):
        for r,c in self:
            for d in self.D:
                if self.is_legal_move((r,c,d), orientation):
                   yield((r,c,d))

class NormalBoard(Board):
    def __init__(self, B, D):
        super().__init__(tuple(tuple(p for p in row) for row in B), D)
    def __iter__(self):
        for r in range(len(self.B)):
            for c in range(len(self.B[r])):
                if self.B[r][c] == 1:
                    yield (r, c)
    def __str__(self):
        return "\n".join([str(row) for row in self.B])
    def __getitem__(self, i):
        r,c = i
        if (0 <= r < len(self.B)) and (0 <= c < len(self.B[r])):
            return self.B[r][c]
        return 2
    def make_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        after = (0, 0, 1)
        if orientation == "reverse":
           after = (1, 1, 0)
        B = [[p for p in row]for row in self.B]
        for i in range(3):
            B[r + i*dr][c + i*dc] = after[i]
        return NormalBoard(B, self.D)
    def sparsify(self):
        blocked = []
        for r in range(len(self.B)):
            for c in range(len(self.B[0])):
                if self[r,c] == 2:
                    blocked.append((r,c))
        return SparseBoard(len(self.B), len(self.B[0]), frozenset(self), self.D, frozenset(blocked))
    def desparsify(self):
        return self

class SparseBoard(Board):
    def __init__(self, R, C, B, D, blocked = frozenset()):
        super().__init__(B, D)
        self.R = R
        self.C = C
        self.blocked = blocked
    def __iter__(self):
        for p in self.B:
            yield p
    def __str__(self):
        return "{} x {}\n{}".format(self.R, self.C, str(self.B))
    def __getitem__(self, i):
        if (i[0] < 0) or (i[0] >= self.R) or (i[1] < 0) or (i[1] >= self.C):
            return 2
        if i in self.blocked:
            return 2
        if i in self.B:
            return 1
        return 0
    def make_move(self, m, orientation = "forward"):
        r, c, d = m
        dr, dc = DIRECTIONS[d]
        B = {p for p in self}
        if orientation == "reverse":
            B.add((r, c))
            B.add((r+dr, c+dc))
            B.remove((r+dr*2, c+dc*2))
        else:
            B.remove((r, c))
            B.remove((r+dr, c+dc))
            B.add((r+dr*2, c+dc*2))
        return SparseBoard(self.R, self.C, frozenset(B), self.D, self.blocked)
    def sparsify(self):
        return self
    def desparsify(self):
        return NormalBoard([[self[r,c] for c in range(self.C)] for r in range(self.R)], self.D)

def test_solvable(f,b):
    path = f(b)
    if path is None:
        return False
    for m in path:
        b = b.make_move(m)
    return b.is_solved()
def test_unsolvable(f,b):
    return f(b) is None

import solitaire as solution
import unittest

submission = solution.solve

class TestSolitaire(unittest.TestCase):
    def test_01(self):
        self.assertTrue(test_unsolvable(submission,SparseBoard(100,100,frozenset(),DIRECTIONS.keys())))
    def test_02(self):
        self.assertTrue([]==submission(SparseBoard(100,100,frozenset([(0,0)]),DIRECTIONS.keys())))
    def test_03(self):
        self.assertTrue(test_solvable(submission,NormalBoard([[0,0,0,0,0],[0,1,1,0],[0,0,1],[0,0],[0]],{"E","S","W","SW"})))
    def test_04(self):
        self.assertTrue(test_solvable(submission,NormalBoard([[1,1,1,1,1],[1,1,1,1],[1,1,1],[1,1],[0]],{"N","E","S","W","NE","SW"})))
    def test_05(self):
        self.assertTrue(test_unsolvable(submission,SparseBoard(2000,2000,frozenset([(r+100,c+100) for r in range(3) for c in range(4)]),{"N","E","S","W"})))
    def test_06(self):
        self.assertTrue(test_solvable(submission,SparseBoard(2000,2000,frozenset({(48,48),(48,49),(48,50),(48,51),(49,48),(49,49),(49,50),(50,48),(50,49),(51,48)}),{"N","E","S","W","NE","SW"})))

if __name__ == "__main__":
    unittest.main(verbosity = 3, exit = False)