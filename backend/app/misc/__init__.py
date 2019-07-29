from .. import db
from sqlalchemy.exc import DatabaseError
from threading import Thread

def add_to_database(obj):
    try:
        db.session.add(obj)
        db.session.commit()

        return True
    except DatabaseError:
        db.session.rollback()

        return False

def wait_in_other_thread(func, callback):
    def target():
        rv = func()
        callback(rv)
    t = Thread(target=target)
    t.run()