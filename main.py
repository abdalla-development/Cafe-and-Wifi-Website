from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    name = StringField(label='Cafe name', validators=[DataRequired()])
    map_url = StringField(label="Map URL", validators=[DataRequired(), URL()])
    img_url = StringField(label="Images URL", validators=[DataRequired(), URL()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_toilet = BooleanField(label="Has Toilets")
    has_wifi = BooleanField(label="Has Wifi")
    can_take_calls = BooleanField(label="Can Take Calls")
    has_sockets = BooleanField(label="Has Sockets")
    seats = StringField(label="Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price", validators=[DataRequired()])
    submit = SubmitField(label='Recommend')


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_sockets = db.Column(db.Boolean, default=False)
    can_take_calls = db.Column(db.Boolean, default=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    cafe = Cafe()
    if request.method == "GET":
        return render_template("add.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            new_cafe = Cafe(name=form.data['name'], map_url=form.data['map_url'], img_url=form.data['img_url'],
                            location=form.data['location'], seats=form.data['seats'],
                            has_toilet=form.data['has_toilet'], has_wifi=form.data['has_wifi'],
                            has_sockets=form.data['has_sockets'], can_take_calls=form.data['can_take_calls'],
                            coffee_price='£'+form.data['coffee_price'])
            db.session.add(new_cafe)
            db.session.commit()
            cafes_in = cafe.query.all()
            return render_template("cafes.html", cafes=cafes_in)


@app.route("/cafes", methods=["GET", "POST"])
def cafes():
    cafe = Cafe()
    if request.method == "GET":
        cafes_in = cafe.query.all()
        return render_template("cafes.html", cafes=cafes_in)
    elif request.method == "POST":
        loc = request.form["address"]
        cafes_in = cafe.query.filter_by(location=f"{loc}")
        return render_template("cafes.html", cafes=cafes_in)


@app.route("/delete/<int:item_id>")
def delete(item_id):
    cafe = Cafe()
    cafe_to_delete = cafe.query.get(item_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


if __name__ == '__main__':
    app.run(debug=True)
