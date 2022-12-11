from input_stuff import PasswordValidator, NameValidator, GuessValidator, InputService, Prompter
from models import WordleDay, Result
from wordlist import WordList
from datetime import datetime
from login import LoginService, PlayerRepository, encode_password
from game import Game

class Application:
    def __init__(self, session):
        self.session = session
        password_validator = PasswordValidator()
        name_validator = NameValidator(session)
        word_list = WordList()
        guess_validator = GuessValidator(word_list)
        prompter = Prompter()
        self.input_service = InputService(name_validator, password_validator, guess_validator, prompter)
        self.wordle_day = session.query(WordleDay).filter(WordleDay.date == datetime.today().date()).one()
        self.game = Game(self.input_service, self.wordle_day, prompter)
        player_repository = PlayerRepository(session, encode_password)
        self.login_service = LoginService(prompter, self.input_service, player_repository)

        
    def start(self):
        active_player = self.login_service.get_user()
        state = self.game.start()
        result = Result(score = 1 if state["won"] else 0, player = active_player, wordle_day = self.wordle_day)
        self.session.add(result)
        self.session.commit()
        if self.input_service.wants_to_continue():
            self.start()  