
import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route('/random', methods=['GET'])
    def random_cafe():
        restult = db.session.execute(db.select(Cafe))
        all_cafes = restult.scalars().all()
        random_cafe = random.choice(all_cafes)
        return jsonify(cafe=random_cafe.to_dict())

# @app.route('/random', methods=['GET'])
# def random_cafe():
#      restult = db.session.execute(db.select(Cafe))
#      all_cafes = restult.scalars().all()
#      random_cafe = random.choice(all_cafes)
#      return jsonify(cafe={
#          "id":random_cafe.id,
#          "name":random_cafe.name,
#          "map_url": random_cafe.map_url
#      })




## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
    with app.create_contect():
        db.create_all()
