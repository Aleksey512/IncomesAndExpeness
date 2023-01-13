from sqlalchemy import (
    create_engine,
    select,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    MetaData,
)
from sqlalchemy.orm import Session, declarative_base, relationship

from datetime import date

engine = create_engine("sqlite:///myDB.db", echo=True, future=True)

Base = declarative_base()


class Income(Base):
    """
    Модель дохода
    """

    __tablename__ = "income"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String)  # На что приход (Зп, нашла на улице ...)
    value = Column(Float)  # Кол-во денег(150.0 руб)
    fact = Column(Boolean, default=False)  # Фактический приход или нет

    def __repr__(self):
        return f"Доход(id={self.id!r}, date={self.date!r}, value={self.value!r}, fact={self.fact!r})"


class Expeness(Base):
    """
    Модель расхода
    """

    __tablename__ = "expeness"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String)  # На что расход (Апельсины, мандарины ...)
    value = Column(Float)  # Кол-во денег(150.0 руб)
    fact = Column(Boolean, default=False)  # Фактический расход или нет

    def __repr__(self):
        return f"Расход(id={self.id!r}, date={self.date!r}, value={self.value!r}, fact={self.fact!r})"


Base.metadata.create_all(engine)
