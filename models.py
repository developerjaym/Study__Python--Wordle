from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Index, Integer,
                        PrimaryKeyConstraint, String, UniqueConstraint, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    __table_args__ = (
            PrimaryKeyConstraint(
                'id',
                name='id_pk'),
            UniqueConstraint(
                'name',
                name='unique_name'),
        )

    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    password = Column(String())
    sign_up_date = Column(DateTime(), default=datetime.now())
    results = relationship('Result', backref=backref('player'))

    # Other timestamp examples
    # server_default tells the database schema to set a value from the database itself.
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}"

class WordleDay(Base):
    __tablename__ = 'wordle_days'

    id = Column(Integer(), primary_key=True)
    word = Column(String())
    date = Column(String(), unique = True)

    results = relationship('Result', backref=backref('wordle_day'))

    def __repr__(self):
        return f'WordleDay(id={self.id}, ' + \
            f'word={self.word}, ' + \
            f'date={self.date})'

class Result(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    #TODO consider storing each of their 6 guesses

    wordle_day_id = Column(Integer(), ForeignKey('wordle_days.id'))
    player_id = Column(Integer(), ForeignKey('players.id'))

    def __repr__(self):
        return f'Result(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'player_id={self.player_id}, ' + \
            f'game_id={self.wordle_day_id})'            

class Guess: #TODO save this eventually
    def __init__(self) -> None:
        pass            