import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from application.db import get_db

bp = Blueprint('people', __name__, url_prefix='/people')


# @bp.route('/create', methods=('POST'))
# def create(person_id):
#     if request.method == 'GET':
#         db = get_db()
#         error = None
#         if db.execute(
#             'SELECT * FROM people WHERE id = ?', (person_id,)
#         ).fetchone() is not None:
#             error = f'Person with id {person_id} already exists.'
        
#         if error is None:
#             db.execute('INSERT into person (id) VALUES (?)',
#                 (person_id)
#             )
#             db.commit()
#             return
#         flash(error)
#     return 

@bp.route('/') # all
# @bp.route('/read/{id}', methods=('GET'))
# @bp.route('/read/{id}/{version}', methods=('GET'))
def read(person_id=None):
    db = get_db()
    people = db.execute(
        'SELECT * FROM person'
    ).fetchall()
    data = []

    for person in people:
        data.append({
            'id': person.id,
            'first_name': person.first_name,
            'middle_name': person.middle_name,
            'last_name': person.last_name,
            'email': person.email,
            'age': person.age
        })
    
    return json.dumps(data)
        
        # users = db.execute(
        #     'SELECT * FROM people WHERE id = ?', (person_id,)
        # ).fetchone()


# @bp.route('/update/{id}', methods=('PUT'))

# @bp.route('/delete/{id}', methods=('POST'))
