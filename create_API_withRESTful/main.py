
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
    return "Take some cafe!"


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

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price= request.args.get("new_price")
    cafe = db.get_or_404(Cafe ,cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response= {"Success":"Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    delete = request.args.get("api-key")
    if delete == "TopSecretAPI":
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success":"Successfully deleted the cafe."}),200
        else:
            return jsonify(error={"Not Found":"Cafe with that id was not found in the datebase."}),404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route("/add", methods=['POST'])
def add_new_cafe():
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets = bool(request.form.get("sockets")),
        has_toilet = bool(request.form.get("toilet")),
        has_wifi = bool(request.form.get("wifi")),
        can_take_calls = bool(request.form.get("calls")),
        seats = request.form.get("seats"),
        coffee_price = request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response ={"Success":"You added the new cafe!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)