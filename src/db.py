
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_db_session_maker():
	engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
	return sessionmaker(bind=engine)

def create_cem_score_table(db_session_maker: sessionmaker):
	db_session = db_session_maker()
	try:
		db_session.execute(text(f'''
			CREATE TABLE IF NOT EXISTS cem_score (
				id SERIAL PRIMARY KEY,
				name VARCHAR(255),
				timescale VARCHAR(255),
				score INT
			)
		'''))
		db_session.commit()
	finally:
		db_session.close()

def find_cem_score(db_session_maker, user_id, name, timescale):
	db_session = db_session_maker()
	try:
		query = text(f'''
			SELECT * FROM cem_score WHERE user_id = :user_id AND name = :name AND timescale = :timescale 
		''')
		result = db_session.execute(query, {'user_id': user_id, 'name': name, "timescale": timescale})
		rows = result.fetchall()
		if len(rows) == 0:
			return None
		return rows[0]
	except Exception as e:
		pass
	finally:
		db_session.close()

def insert_cem_score(db_session_maker, user_id, name, timescale, score):
	db_session = db_session_maker()
	try:
		score_exists = find_cem_score(db_session_maker, user_id, name, timescale)
		if (score_exists):
			query = text(f'''
				UPDATE cem_score
				SET score = :score
				WHERE user_id = :user_id AND name = :name AND timescale = :timescale
			''')
			db_session.execute(query, {'user_id':user_id, 'name':name, 'timescale':timescale, "score":score})
			db_session.commit()
			return
		query = text(f'''
			INSERT INTO cem_score (user_id, name, timescale, score)
			VALUES (:user_id, :name, :timescale, :score)
		''')
		db_session.execute(query, {'user_id':user_id, 'name':name, 'timescale':timescale, "score":score})
		db_session.commit()
	except Exception as e:
		print(e)
	finally:
		db_session.close()
