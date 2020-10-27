from unittest import TestCase
from app import app
from flask import session, jsonify, json, request
from boggle import Boggle
from unittest.mock import patch, Mock

board = [["A","A","R","Z","P","W"],
        ["R","B","I","T","S","X"],
        ["U","C","L","S","I","Y"],
        ["D","L","Q","D","O","Z"],
        ["F","K","A","M","N","U"],
        ["O","T","Y","O","Z","H"],
        ["V","H","I","X","L","K"],
        ["A","G","P","Y","P","Q"]]


class FlaskTests(TestCase):
    
    # ------------ Test app.py ----------------------
    
    def test_game_html(self):
        """
            # Test if function creates HTML page
        """
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-success btnMain" type="submit">Guess</button>', html)
    
    def test_start_post(self):
        """
            # Test function to see if we can create a List board of
            # size 9x8
        """
        with app.test_client() as client:
            res = client.post("/start", json={"rows":9,"cols":8})
            req = json.loads(res.get_data(as_text=True))
            board = req["board"]
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(board), 9)
            self.assertEqual(len(board[0]), 8)
            
    def test_guess_post(self):
        """ 
            # 1. Pick out a long-ish word from words.txt
            # 2. word = abarticulation
            # 3. Create a 5x5 List board that includes the word
            # 4. Store the board in a session variable "board" to be consumed by the testing function
            # 5. Run the test to see if the function returns True
        """
        with app.test_client() as client:
            
            
            with client.session_transaction() as sess:
                sess["boggle"] = board
                sess["guesses"] = []
                sess["correct_guesses"] = []
                sess.modified = True
                
            res = client.post("/guess", json={"guess":"abarticulation"})
            req = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertTrue(req)
            
    # ------ Test boggle.py -------------

    def test_read_dict(self):
        """
            # Test if function reads a file and stores words
            # check id word "abarticulation" exists in List
        """
        with app.test_client() as client:
            boggle = Boggle()
            words = boggle.read_dict("words.txt")
            self.assertIn("abarticulation", words)

    def test_make_board(self):
        """
            # Test if function creates a List board of given size
        """
        with app.test_client() as client:
            boggle = Boggle()
            board1 = boggle.make_board(5, 6)
            board2 = boggle.make_board(6, 5)
            
            self.assertEqual(len(board1), 5)
            self.assertEqual(len(board1[0]), 6)
            self.assertEqual(len(board2), 6)
            self.assertEqual(len(board2[0]), 5)
    
    def test_valid_word(self):
        """
            # Test if word is both in the List Dictionary and in
            # List board
        """
        with app.test_client() as client:
            boggle = Boggle()
            isWord = boggle.check_valid_word(board, "abarticulation")
            self.assertTrue(isWord)
    
    def test_search(self):
        """
            # Test if word is in List board
        """
        with app.test_client() as client:
            boggle = Boggle()
            word = "abarticulation".upper()
            isWordTrue = boggle.search(board, word, 0, 0, [])
            isWordNone = boggle.search(board, word, 4, 5, [])        
            self.assertEqual(isWordTrue, True)
            self.assertEqual(isWordNone, None)
    
    def test_find(self):
        """
            # Test if word is in List board at a given row and column location
            # Also test that word is not in List board at a different row
            # column location
        """
        with app.test_client() as client:
            boggle = Boggle()
            word = "abarticulation".upper()
            isWordTrue = boggle.find(board, word)
            isWordFalse = boggle.find(board, word+"Q")
            self.assertEqual(isWordTrue, True)
            self.assertEqual(isWordFalse, False)
