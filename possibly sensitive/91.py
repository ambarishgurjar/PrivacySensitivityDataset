
from decimal import Decimal
from flask import Flask, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField
from wtforms.validators import InputRequired



app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
app.config.from_pyfile('local.py', silent=True)
db = SQLAlchemy(app)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code3 = db.Column(db.String(3), unique=True)
    currency = db.Column(db.String(3))
    name = db.Column(db.String(80), unique=True)
    year = db.Column(db.Integer())
    ppp = db.Column(db.Numeric(2))

    def __repr__(self):
        return '<Country {0}>'.format(self.name)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.String(80))

    def __repr__(self):
        return '<Config {0}: {1}>'.format(self.key, self.value)


# Form
class SalaryForm(FlaskForm):
    from_country = SelectField('Source country', coerce=int)
    salary = DecimalField("Amount in source country's local currency",
                          validators=[InputRequired()])
    to_country = SelectField('Target country', coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SalaryForm()
    currency_value = None
    tocountry = None
    fromcountry = None
    form.from_country.choices = [(country.id, country.name) for country in
                                 Country.query.order_by('name').all()]
    form.to_country.choices = [(country.id, country.name) for country in
                               Country.query.order_by('name').all()]
    if form.validate_on_submit():
        fromcountry = Country.query.get(form.from_country.data)
        tocountry = Country.query.get(form.to_country.data)
        if fromcountry or tocountry is not None:
            currency_value = moneyfmt((form.salary.data / fromcountry.ppp) *
                                      tocountry.ppp)
    conversion = Config.query.filter_by(key='gbp_rate').first()
    d = {
        'form': form,
        'currency_value': currency_value,
        'fromcountry': None,
        'tocountry': tocountry,
        'conversion_rate': float(conversion.value) * 100,
    }
    if fromcountry:
        d['fromcountry'] = fromcountry
        d['input_value'] = moneyfmt(form.salary.data)
    return render_template('index.html', **d)


@app.route('/json')
def jsondata():
    countries = Country.query.all()
    countrieslist = [
            {
                'id': country.id,
                'name': country.name,
                'ppp': str(country.ppp),
                'code3': country.code3,
                'currency': country.currency
            }
            for country in countries
    ]