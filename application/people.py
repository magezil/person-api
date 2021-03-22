import json
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from application.db import get_db

bp = Blueprint('people', __name__)


PERSON_NOT_FOUND = 'Person with id {person_id} not found'


@bp.route('/create', methods=('POST',))
def create():
    person_id = request.form['id']
    db = get_db()
    error = None
    if get_person(person_id) is not None:
        error = f'Person with id {person_id} already exists.'
    
    if error is None:
        # save version as YYYYMMDD: person_data
        data = request.form
        try:
            person_data = {
                'id': data['id'],
                'first_name': data['first_name'],
                'middle_name': data.get('middle_name'),
                'last_name': data['last_name'],
                'email': data['email'],
                'age': data['age'],
            }
            metadata = {
                datetime.now().strftime('%Y%m%d'): person_data
            }
            person_data['metadata'] = json.dumps(metadata)
        except KeyError:
            return 'Missing required property', 400
        db.execute('INSERT into person (id, first_name, middle_name, last_name, email, age, metadata) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                person_data["id"],
                person_data["first_name"],
                person_data["middle_name"],
                person_data["last_name"],
                person_data["email"],
                person_data["age"],
                person_data["metadata"]                
            )
        )
        db.commit()
        return f'Successfully added user {person_id}'
    return f'Error {error}', 400

@bp.route('/') # all
@bp.route('/<int:person_id>', methods=('GET',))
@bp.route('/<int:person_id>/<version>', methods=('GET',))
def read(person_id=None, version=None):
    db = get_db()
    if person_id is None:
        people = db.execute(
            'SELECT * FROM person'
        ).fetchall()
        data = []

        for person in people:
            data.append({
                'id': person[0],
                'first_name': person[1],
                'middle_name': person[2],
                'last_name': person[3],
                'email': person[4],
                'age': person[5]
            })
    else:
        person = get_person(person_id)
        if person is None:
            return PERSON_NOT_FOUND.format(person_id=person_id), 404
        if version is not None:
            person = json.loads(person['metadata'])
            if version not in person:
                return f'Person {person_id} does not have version {version}', 404
            person = person[version]
        data = {
            'id': person['id'],
            'first_name': person['first_name'],
            'middle_name': person['middle_name'],
            'last_name': person['last_name'],
            'email': person['email'],
            'age': person['age']
        }

    return json.dumps(data)


@bp.route('/update/<int:person_id>', methods=('POST',))
def update(person_id):
    person = get_person(person_id)
    db = get_db()

    try:
        data = request.form
        person_data = {
            'id': person_id,
            'first_name': data['first_name'],
            'middle_name': data.get('middle_name'),
            'last_name': data['last_name'],
            'email': data['email'],
            'age': data['age'],
        }
        metadata = json.loads(person["metadata"])
        key = datetime.now().strftime('%Y%m%d')
        if key in metadata:
            key = key + '.' + str(len(metadata))
        metadata[key] = person_data
        person_data['metadata'] = json.dumps(metadata)
    except KeyError:
        return 'Missing required property'
    db.execute("""UPDATE person SET 
                first_name = ?,
                middle_name = ?,
                last_name = ?,
                email = ?,
                age = ?,
                metadata = ?
            """,
        (
            person_data["first_name"],
            person_data["middle_name"],
            person_data["last_name"],
            person_data["email"],
            person_data["age"],
            person_data["metadata"]                
        )
    )
    db.commit()
    return f'Successfully updated user {person_id}'

@bp.route('/delete/<int:person_id>', methods=('POST',))
def delete(person_id):
    person = get_person(person_id)
    print('heyo', person)
    if person is None:
        return PERSON_NOT_FOUND.format(person_id=person_id), 404
    db = get_db()
    db.execute('DELETE FROM person WHERE id = ?', (person_id,))
    db.commit()
    return f'Deleted user {person_id}'

# Helper functions
def get_person(person_id):
    db = get_db()
    person = db.execute(
            'SELECT * FROM person WHERE id = ?', (person_id,)
        ).fetchone()
    return person
