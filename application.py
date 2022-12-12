from input_stuff import PasswordValidator, NameValidator, GuessValidator, InputService, Prompter
from models import WordleDay, Result
from wordlist import WordList
from datetime import datetime
from login import LoginService, PlayerRepository, encode_password
from game import Game
from stats import ResultRepository, StatisticsDisplayer

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
        self.result_respository = ResultRepository(session)
        self.login_service = LoginService(prompter, self.input_service, player_repository)
        self.statistics_displayer = StatisticsDisplayer(prompter)

        
    def start(self):
        active_player = self.login_service.get_user()
        state = self.game.start()
        result = Result(score = 0 if not state["won"] else len(state["guesses"]), player = active_player, wordle_day = self.wordle_day)
        self.result_respository.save(result)
        self.statistics_displayer.display(self.result_respository.get_results(active_player.id))
        if self.input_service.wants_to_continue():
            self.start()  