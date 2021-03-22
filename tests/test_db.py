import sqlite3

import pytest
from application.db import get_db


def test_get_close_db(app):
    print(1)
    with app.app_context():
        db = get_db()
        assert db is get_db()

    print(2)
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    print(3)
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('application.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
