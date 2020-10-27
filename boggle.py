"""Utilities related to Boggle game."""

from random import choice
import string


class Boggle():

    def __init__(self):

        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""

        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self, rows=5, cols=5):
        """Make and return a random boggle board."""

        board = []

        for y in range(rows):
            row = [choice(string.ascii_uppercase) for i in range(cols)]
            board.append(row)

        return board
    
    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""

        word_exists = word.lower() in self.words
        valid_word = self.find(board, word.upper())
        return word_exists and valid_word


    def search(self, board, word, row, col, visited):
        """Check if word is in the board List at a specific location"""
        if word == "":
            return True
        neighbors = [[0,0],[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]
        for [r,c] in neighbors:
            rr = r + row
            cc = c + col
            if rr < 0 or cc < 0: 
                continue
            if rr >= len(board) or cc >= len(board[0]):
                continue
            if [rr,cc] in visited:
                continue
            if word[0] == board[rr][cc]:
                visited.append([rr,cc])
                if self.search(board, word[1:], rr, cc, visited):
                    return True
 
    def find(self, board, word):
        """Check if word is in the board List"""     
        for r in range(0,len(board)):
            for c in range(0,len(board[0])):
                if self.search(board, word, r, c, visited=[]):
                    return True
        return False
