from models import Player
class PlayerRepository:
    def __init__(self, session):
        self._session = session
    def get_player(self, name, password):
        return self._session.query(Player).filter(Player.name==name, Player.password == password).one_or_none()
    def save(self, player):
        self._session.add(player)
        self._session.commit()

class LoginService:
    def __init__(self, prompter, input_service, player_repository):
        self._prompter = prompter
        self._input_service = input_service
        self._player_repository = player_repository
    def get_user(self):
        if not self._input_service.has_account():
            self._prompter.show_message('Sign Up Time!')
            player_name = self._input_service.get_name()
            player_password = self._input_service.get_password()
            self._prompter.show_message(f"Welcome, {player_name}")
            player = Player(name=player_name, password=player_password)
            self._player_repository.save(player)
            return player
        else:
            self._prompter.show_message('Sign In Time!')
            player_name = self._input_service.get_name(validate=False)
            player_password = self._input_service.get_password(confirmation_prompt=False)
            player = self._player_repository.get_player(player_name, player_password)
            if player == None:
                self._prompter.show_error(f"No record of that username and password combination in our database.")
                return self.get_user()
            return player    
            #TODO worry about password encoding
            #TODO worry about error handling

