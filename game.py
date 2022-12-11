from input_stuff import PasswordValidator, NameValidator, GuessValidator, InputService, Prompter
from models import Player, WordleDay, Result
from wordlist import WordList
from datetime import datetime
from login import LoginService, PlayerRepository
from enum import Enum

class Application:
    def __init__(self, session):
        self.session = session
        password_validator = PasswordValidator()
        name_validator = NameValidator(session)
        word_list = WordList()
        guess_validator = GuessValidator(word_list)
        prompter = Prompter()
        input_service = InputService(name_validator, password_validator, guess_validator, prompter)
        self.wordle_day = session.query(WordleDay).filter(WordleDay.date == datetime.today().date()).one()
        self.game = Game(input_service, self.wordle_day, prompter)
        player_repository = PlayerRepository(session)
        self.login_service = LoginService(prompter, input_service, player_repository)

        
    def start(self):
        active_player = self.login_service.get_user()
        analysis = self.game.start()
        result = Result(score = 1 if analysis["won"] else 0, player = active_player, wordle_day = self.wordle_day)
        self.session.add(result)
        self.session.commit()
        
class LetterResult(Enum):
    PERFECT = "green"
    WRONG_PLACE = "yellow"
    TOTALLY_WRONG = "black"

class Game:
    def __init__(self, input_service, wordle_day, prompter) -> None:
        self._input_service = input_service
        self._wordle_day = wordle_day
        self._prompter = prompter
        self._state = {
            "round": 0,
            "guesses": [],
            "over": False
        }
    def start(self):
        while self._state["round"] < 6 and not self._state["over"]:
            self._prompter.show_message(f"Round {(self._state['round'] + 1)}")
            guess = self._input_service.get_word(invalid=self._state["guesses"]).strip().upper()
            self._state["guesses"].append(guess)
            self._state["round"] = self._state["round"] + 1
            analysis = self._analyze_guess(guess)
            self._state["over"] = len([val for val in analysis.values() if val[0] == LetterResult.PERFECT]) == 5
            self._prompter.show_colored_message([(val[0].value, val[1]) for val in analysis.values()])
            if self._state["over"]:
                self._state["won"] = True
                self._prompter.show_colored_message([("green", "W"), ("green", "I"), ("green", "N"), ("green", "N"), ("green", "E"), ("green", "R"),("green", "!")])
                return self._state
        self._prompter.show_colored_message([("red", "L"), ("red", "O"), ("red", "S"), ("red", "E"), ("red", "R"), ("red", "!")])
        self._state["won"] = False
        return self._state
       
  
    def _analyze_guess(self, guess):
        analysis = {}
        right_word = self._wordle_day.word
        adjusted_word = right_word
        #find perfect matches
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if guessed_letter == adjusted_word[letter_index]:
                analysis[f"{letter_index}"] = (LetterResult.PERFECT, guessed_letter)   
                adjusted_word = list(adjusted_word)
                adjusted_word[letter_index] = '_'  
                adjusted_word = ''.join(adjusted_word)        

        #round 2, find wrong place matches        
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if f"{letter_index}" not in analysis and guessed_letter in adjusted_word:
                analysis[f"{letter_index}"] = (LetterResult.WRONG_PLACE, guessed_letter)
                adjusted_word.replace(guessed_letter, '_', 1)  

        #round 3, set the remainder 
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if f"{letter_index}" not in analysis:
                analysis[f"{letter_index}"] = (LetterResult.TOTALLY_WRONG, guessed_letter)

        ordered_analysis = {}
        for key in range(5):
            ordered_analysis[f"{key}"] = analysis[f"{key}"]
        return ordered_analysis
