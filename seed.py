from datetime import datetime, timedelta
from models import WordleDay

def seeder(session):
    words = ['JOUST', 'ABOUT', 'CRANE', 'FRANK', 'IDEAL', 'EPOXY']
    today = datetime.today()
    numdays = len(words)
    date_list = [today + timedelta(days=x) for x in range(numdays)]
    for i in range(numdays):
        d = date_list[i].date()
        word = words[i]
        wordle_day = WordleDay(word=word, date=d)
        session.add(wordle_day)
    session.commit()