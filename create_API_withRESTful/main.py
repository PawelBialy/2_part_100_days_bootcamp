
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


    @app.route("/")
    def home():
        return "Take some cafe!"

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name]= getattr(self,column.name)
        return dictionary

    @app.route("/random")
    def get_random_caffe():
        result = db.session.execute(db.select(Cafe))
        all_cafes=result.scalars().all()
        random_cafe = random.choice(all_cafes)
        return  jsonify (cafe=random_cafe.to_dict())

    @app.route("/all")
    def get_all_cafes():
        get_all_result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
        get_all = get_all_result.scalars().all()
        return  jsonify(cafes=[cafe.to_dict() for cafe in get_all])

    @app.route("/search")
    def search_cafe():
        loc = request.args.get('loc') #get loc from query
        cafes_in_area = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
        all_cafess = cafes_in_area.scalars().all()
        if all_cafess:
           return jsonify(cafes=[cafe.to_dict() for cafe in all_cafess])
        else:
            return jsonify({"error": "Location paramether is missing."}),404



if __name__ == '__main__':
    app.run(debug=True)
    with app.create_contect():
        db.create_all()
