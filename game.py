from enum import Enum

class LetterResult(Enum):
    PERFECT = "green"
    WRONG_PLACE = "yellow"
    TOTALLY_WRONG = "black"

class Game:
    def __init__(self, input_service, wordle_day, prompter) -> None:
        self._input_service = input_service
        self._wordle_day = wordle_day
        self._prompter = prompter
    def start(self):
        self._state = {
            "round": 0,
            "guesses": set(),
            "over": False
        }
        while self._state["round"] < 6 and not self._state["over"]:
            self._prompter.show_message(f"Round {(self._state['round'] + 1)}")
            guess = self._input_service.get_word(already_played=self._state["guesses"]).strip().upper()
            self._state["guesses"].add(guess)
            self._state["round"] = self._state["round"] + 1
            analysis = self._analyze_guess(guess)
            self._state["over"] = len([val for val in analysis if val[0] == LetterResult.PERFECT]) == 5
            self._prompter.show_colored_message([(val[0].value, val[1]) for val in analysis])
            if self._state["over"]:
                self._state["won"] = True
                self._prompter.show_colored_message([("green", "W"), ("green", "I"), ("green", "N"), ("green", "N"), ("green", "E"), ("green", "R"),("green", "!")])
                return self._state
        self._prompter.show_colored_message([("red", "L"), ("red", "O"), ("red", "S"), ("red", "E"), ("red", "R"), ("red", "!")])
        self._state["won"] = False
        return self._state
       
  
    def _analyze_guess(self, guess):
        right_letters = list(self._wordle_day.word)

        analysis_list = [(LetterResult.TOTALLY_WRONG, guessed_letter) for guessed_letter in guess] 
        #round 1, find perfect matches
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if guessed_letter == right_letters[letter_index]:
                analysis_list[letter_index] = (LetterResult.PERFECT, guessed_letter)
                right_letters[letter_index] = '_'

        #round 2, find wrong place matches        
        for letter_index in range(5):
            guessed_letter = guess[letter_index]
            if analysis_list[letter_index][0] == LetterResult.TOTALLY_WRONG and guessed_letter in right_letters:
                analysis_list[letter_index] = (LetterResult.WRONG_PLACE, guessed_letter)
                right_letters.remove(guessed_letter)

        return analysis_list

