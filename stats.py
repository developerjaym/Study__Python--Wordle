from models import Player, Result
from datetime import datetime, timedelta, date

class ResultRepository:
    def __init__(self, session):
        self._session = session
    def get_results(self, player_id):
        return self._session.query(Result).filter(Result.player_id==player_id).all()   
    def save(self, result):
        self._session.add(result)
        self._session.commit()


class StatisticsDisplayer:
    def __init__(self, prompter):
        self._prompter = prompter
    def display(self, results):
        self.display_streak(results)
        self.display_past_results(results)
    def display_streak(self, results):
        if len([result for result in results if result.score > 0]) == 0:
            self._prompter.show_colored_message([('red', f"You've never won...")])
        else:
            today = datetime.today()
            first_play_date = self._find_first_play_date(results)
            delta = today - first_play_date
            numdays = delta.days
            date_list = [today - timedelta(days=x) for x in range(numdays)]
            last_failure = first_play_date - timedelta(days=1)
            for some_datetime in date_list:
                as_date_only = some_datetime.date()
                this_day_is_a_loser = len([result for result in results if datetime.fromisoformat(result.wordle_day.date) == as_date_only]) == 0
                if this_day_is_a_loser:
                    last_failure = as_date_only
                    break
            self._prompter.show_colored_message([('white', f"You've been on a winning streak since {last_failure.date()}")])        
    def display_past_results(self, results):
        counts = {}
        for result in results:
            if result.score in counts:
                counts[result.score] += 1
            else:
                counts[result.score] = 1
        for item in range(1, 7):
            number_of_days_with_this_many_guesses = counts.get(item, 0)
            tuple_list = [('green', ' ') for num in range(number_of_days_with_this_many_guesses)]
            self._prompter.show_colored_message([('white', f"{item} guess(es): "), ('white', f"{number_of_days_with_this_many_guesses}")] + tuple_list) 
    def _find_first_play_date(self, results):
        results.sort(key=lambda r: r.wordle_day.date)
        return datetime.fromisoformat(results[0].wordle_day.date)