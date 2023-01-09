from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db_models import Base, Income, Expeness

from datetime import date

engine = create_engine("sqlite:///myDB.db", echo=True, future=True)
initializaton = Base.metadata.create_all(engine)


def income():
	session = Session(engine, future=True)
	statement = select(Income)
	result = session.execute(statement).all()
	return len(result)

def add():
	with Session(engine) as session:
		spongebob = Income(
			name="add",
			value=150,
			date=date.today()
			)
		session.add(spongebob)
		session.commit()