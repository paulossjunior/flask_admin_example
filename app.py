import os
from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))

    def __str__(self):
        return self.desc


class Tyre(db.Model):
    __tablename__ = 'tyres'
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), primary_key=True)
    tyre_id = db.Column(db.Integer, primary_key=True)
    car = db.relationship('Car', backref='tyres')
    desc = db.Column(db.String(50))


class CarAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'desc']


class TyreAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['car', 'tyre_id', 'desc']

admin = Admin(app, name='Exemplo do Flask Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(CarAdmin(Car, db.session))
admin.add_view(TyreAdmin(Tyre, db.session))

if __name__ == '__main__':

    # Create DB
    db.create_all()
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))