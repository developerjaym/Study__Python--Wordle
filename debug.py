#!/usr/bin/env python3

from datetime import datetime, timedelta

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, Player, WordleDay, Result
import input_stuff
from wordlist import WordList
import click
from seed import seeder
from game import Application

if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
     # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()
    print(session.query(Player).all())
    # Load up the database with days
    # ask user to sign in
    # let user start guessing TODO: show the user their current state for today
    # after 6 tries or a correct guess, save user's results

    # Load up the database with days
    # words = ['JOUST', 'ABOUT', 'CRANE', 'FRANK', 'IDEAL', 'EPOXY']
    # today = datetime.today()
    # numdays = len(words)
    # date_list = [today + timedelta(days=x) for x in range(numdays)]
    # word_list = WordList()
    # for i in range(numdays):
    #     d = date_list[i].date()
    #     word = words[i]
    #     wordle_day = WordleDay(word=word, date=d)
    #     print(wordle_day)
    #     session.add(wordle_day)
    # session.commit()
    seeder(session)
    # print(session.query(WordleDay).all())
    application = Application(session)
    application.start()
        

    # ask user to sign in
    # while True: #TODO 
    #     wordle_day = session.query(WordleDay).filter(WordleDay.date == datetime.today().date()).first()
    #     if click.confirm("Are you a new user?", default=False):
    #         click.secho('Sign Up Time!', fg='green')
    #         # player_name = click.prompt(click.style("Name: ", fg="green"))
    #         player_name = click.prompt(click.style("Name", bold=True))
    #         player_password = click.prompt(click.style("Password", bold=True), confirmation_prompt=True, hide_input=True)
    #         print("hello????", player_name, player_password)
    #         active_player = Player(name=player_name, password=player_password)
    #         session.add(active_player)
    #         session.commit()
    #     else:
    #         click.secho('Sign In Time!', fg='blue')
    #         player_name = click.prompt(click.style("Name", bold=True))
    #         player_password = click.prompt(click.style("Password", bold=True), confirmation_prompt=False, hide_input=True)
    #         #TODO worry about password encoding
    #         #TODO worry about error handling
    #         active_player = session.query(Player).filter(Player.name==player_name, Player.password == player_password).first()

    #     print(f"Welcome, {active_player.name}! Your statistics: {active_player.results}.")
    #     # let user start guessing TODO: show the user their current state for today
    #     state = [click.style('⛶', fg="white"), click.style('⛶', fg="white"), click.style('⛶', fg="white"), click.style('⛶', fg="white"), click.style('⛶', fg="white")]
    #     right_word = wordle_day.word
    #     for i in range(6):
    #         click.secho(''.join(state), fg='white')
    #         guess = click.prompt('Your guess').strip().upper()
    #         #TODO verify that they typed a real word
    #         #TODO verify that they typed 5 letters
    #         if word_list.is_word(guess):
    #             print("That's a word", guess)
    #         else:
    #             print("THAT IS NOT A WORD")    
    #         count = 0
    #         for letter_index in range(5):
    #             if guess[letter_index] == right_word[letter_index]:
    #                 state[letter_index] = click.style(guess[letter_index], fg="green")
    #                 count += 1
    #             elif guess[letter_index] in right_word:
    #                 #TODO figure out how to turn the right number of letters yellow
    #                 state[letter_index] = click.style(guess[letter_index], fg="yellow")
    #             else:
    #                 state[letter_index] = click.style(guess[letter_index], fg="white")       
    #         if count == 5:
    #             click.secho("Yay", bold=True, fg="green", bg="white")
    #             break
    #     # after 6 tries or a correct guess, save user's results    
    #     if count != 5:
    #         click.secho(f"You're dumb. It was {right_word}.", bold=True, fg="red", bg="white")
    #         result = Result(score = 0, player = active_player, wordle_day=wordle_day)
    #     else:
    #         result = Result(score = i + 1, player = active_player, wordle_day=wordle_day)
    #     session.add(result)
    #     session.commit()

    #     if click.confirm("Want to quit?", default=True):
    #         b = click.style('B', fg="red")
    #         y = click.style('Y', fg="green")
    #         e = click.style('E', fg="red")
    #         click.echo(f"{b}{y}{e}")
    #         break
    #     print("looping time!")

    