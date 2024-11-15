# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)





@app.route('/demo_json')
def demo_json():
    pet_json = '{"id": 1, "name" : "Fido", "species" : "Dog"}'
    return make_response(pet_json, 200)

@app.route('/')
def index():
    body= {'message':'welcome to pet directory!'}
    return make_response(body)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet =Pet.query.filter(Pet.id == id).first()
    if pet:
        body={'id':pet.id,'name':pet.name,'species':pet.species}
        status=200
    else:
        body={'message':f'Pet {id} is not found.'}
        status=404
    return make_response(body,status)
@app.route('/species/<string:species>')
def pet_by_species(species):
    pets= [{'id':pet.id,'name':pet.name} for pet in Pet.query.filter_by(soecies==species).all()]
    body={'count':len(pets) , 'pets':pets}

    return make_response(body,200)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
