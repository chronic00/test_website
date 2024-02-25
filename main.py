from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
import requests

# pip install bootstrap-flask
# pip install flask_sqlalchemy
# pip install flask_wtf

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holdings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Holdings(db.Model):
    ticker = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(4), unique=False, nullable=False)


# Add record
# with app.app_context():
#     new_holding = Holdings(ticker='VVSM', title='vanEck Semiconductor', value=5000, cost=2000, currency='EUR')
#     db.session.add(new_holding)
#     db.session.commit()

# # First time initialization
# with app.app_context():
#    db.session.commit()


@app.route('/')
def home():
    all_holdings = db.session.query(Holdings).all()
    total_value = 0.00
    total_cost = 0.00
    total_profit = 0
    randament = 0
    for holding in all_holdings:
        total_value += holding.value
        total_cost += holding.cost
    total_profit = total_value - total_cost
    randament = total_profit / total_cost * 100

    return render_template('index.html', value=round(total_value,2), cost=round(total_cost,2), profit=round(total_profit,2), randament=round(randament,2))


@app.route("/overview")
def display_all_holdings():
    all_holdings = db.session.query(Holdings).order_by("value").all()
    return render_template("overview.html", holdings=all_holdings)


if __name__ == "__main__":
    app.run(debug=True)
