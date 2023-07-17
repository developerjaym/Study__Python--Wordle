import click
from models import Player


class GuessValidator:
    def __init__(self, word_list):
        self._word_list = word_list
    def _is_long_enough(self, str):
        return len(str) == 5
    def _is_word(self, str):
        return self._word_list.is_word(str)    
    def validation_results(self, str, already_guessed):
        results = {}
        if not self._is_long_enough(str):
            results["length"] = f"'{str}' is not the right length. Must be 5 characters."
        if not self._is_word(str):
            results["nonword"] = f"'{str}' is not in my dictionary."  
        if len([word for word in already_guessed if word.upper() == str.upper()]) > 0:
            results["played"] = f"'{str}' has already been played."      
        return results         

class PasswordValidator:
    def _is_long_enough(self, str):
        return len(str) >= 3
    def validation_results(self, str):
        results = {}
        if not self._is_long_enough(str):
            results["length"] = f"'{str}' is too short. Must be 3 characters or longer."
        return results    

class NameValidator:
    def __init__(self, session):
        self._session = session
    def _is_unique_name(self, name):
        return self._session.query(Player).filter(Player.name == name).count() == 0
    def _is_long_enough(self, name):
        return len(name) >= 3
    def validation_results(self, name):
        results = {}
        if not self._is_unique_name(name):
            results["unique"] = f"'{name}' is already taken."
        if not self._is_long_enough(name):
            results["length"] = f"'{name}' is too short. Must be 3 characters or longer."
        return results    
  
class Prompter:
    def __init__(self):
        self._happy_fg = "green"
        self._normal_fg = "white"
        self._normal_bg = "black"
        self._sad_fg = "red"
    def get_yes_no(self, prompt, default=False):
        return click.confirm(prompt, default=default)    
    def get_string(self, prompt):
        return click.prompt(click.style(prompt, bold=True, fg=self._normal_fg, bg=self._normal_bg))
    def get_password(self, confirmation_prompt=True):
        return click.prompt(click.style("Password", bold=True, fg=self._normal_fg, bg=self._normal_bg), confirmation_prompt=confirmation_prompt, hide_input=True)
    def show_error(self, message):
        click.secho(message, bold=True, fg=self._sad_fg, bg=self._normal_bg)
    def show_message(self, message):
        click.secho(message, bold=False, fg=self._normal_fg, bg=self._normal_bg)
    def show_colored_message(self, color_letter_tuples):
        message = ""
        for val in color_letter_tuples:
            message = f"{message}{click.style(val[1], bg=val[0], fg=self._normal_bg, bold=True)}"
        click.secho(message)

class InputService:
    def __init__(self, name_validator, password_validator, guess_validator, prompter):
        self._name_validator = name_validator
        self._password_validator = password_validator
        self._guess_validator = guess_validator
        self._prompter = prompter
    def wants_to_continue(self):
        return self._prompter.get_yes_no("Do you want to play again?")    
    def has_account(self):
        return self._prompter.get_yes_no("Do you have an account?")
    def get_name(self, validate=True):
        response = self._prompter.get_string("Name")
        if validate:
            validation_results = self._name_validator.validation_results(response)
            if len(validation_results):
                for result in validation_results.values():
                    self._prompter.show_error(result)
                return self.get_name()    
        return response  
    def get_password(self, confirmation_prompt=True):
        response = self._prompter.get_password(confirmation_prompt)
        validation_results = self._password_validator.validation_results(response)
        if len(validation_results):
            for result in validation_results.values():
                self._prompter.show_error(result)
            return self.get_password(confirmation_prompt)
        return response
    def get_word(self, already_played):
        response = self._prompter.get_string("Your guess").upper().strip()
        validation_results = self._guess_validator.validation_results(response, already_played)
        if len(validation_results):
            for result in validation_results.values():
                self._prompter.show_error(result)
            return self.get_word(already_played)    
        return response    

