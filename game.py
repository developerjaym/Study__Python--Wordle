from input_stuff import PasswordValidator, NameValidator, GuessValidator, InputService, Prompter
from models import Player, WordleDay, Result
from wordlist import WordList
from datetime import datetime
from login import LoginService, PlayerRepository
from enum import Enum

class Application:
    def __init__(self, session):
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
        print("eventually save this", result)
        #TODO save result for active_player
        
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
            guess = self._input_service.get_word().strip().upper()
            self._state["guesses"].append(guess)
            self._state["round"] += self._state["round"]
            analysis = self._analyze_guess(guess)
            self._state["over"] = len([val for val in analysis.values() if val[0] == LetterResult.PERFECT]) == 5
            self._prompter.show_colored_message(analysis)
            if self._state["over"]:
                self._state["won"] = True
                print("Winner!")
                return self._state
                #TODO congratulate winner
        print("lost") #TODO ridicule loser
        self._state["won"] = False
        return self._state
    def _analyze_guess(self, guess):
        analysis = {}
        right_word = self._wordle_day.word
        #TODO this map doesn't work since it doesn't allow multiples of the same letter
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if guessed_letter == right_word[letter_index]:
                analysis[f"{letter_index}"] = (LetterResult.PERFECT, guessed_letter)
            elif guessed_letter in right_word:
                #TODO figure out how to turn the right number of letters yellow
                #find count of each letter in right_word?
                #
                analysis[f"{letter_index}"] = (LetterResult.WRONG_PLACE, guessed_letter)
            else:
                analysis[f"{letter_index}"] = (LetterResult.TOTALLY_WRONG, guessed_letter)    
        print(analysis)
        return analysis
