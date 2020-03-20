from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from send_mail import send_mail

app = Flask(__name__)

# .........................Setting up Database ......................
ENV = ''
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:berzone@localhost/generator'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jynasdeissbqqu:74d771fb1054684f37e31f1bf706d3d4c0afb39c8cd82a71120f09f1640589c3@ec2-18-210-51-239.compute-1.amazonaws.com:5432/d5718s4db4oaif'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class GeneratorTable(db.Model):
    __tablename__ = 'database'
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(200))
    continent = db.Column(db.String(50))
    country = db.Column(db.String(50))
    type = db.Column(db.String(50))
    description = db.Column(db.Text())

    def __init__(self, place, continent, country, type, description):
        self.place = place
        self.continent = continent
        self.country = country
        self.type = type
        self.description = description

# ......................main home page..................................
@app.route('/')
def index():
    return render_template('index.html')

# .......................brings to ADD DATA page...........................
@app.route('/add_data')
def add_data():
    return render_template('add_data.html')

# ............After adding data..saves to database and forwards to choice page
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        place = request.form['place']
        continent = request.form['continent']
        country = request.form['country']
        type = request.form['type']
        description = request.form['description']

        data = GeneratorTable(place, continent, country, type, description)
        db.session.add(data)
        db.session.commit()

        return render_template('added.html') #..............CHOICE PAGE

@app.route('/filter', methods=['POST', 'GET'])
def filter():

    if request.method == 'POST':
        continent = str(request.form['continent'])
        type = str(request.form['type'])
        link = "https://www.google.com/search?q="

        connection = psycopg2.connect(user= "jynasdeissbqqu", password = "74d771fb1054684f37e31f1bf706d3d4c0afb39c8cd82a71120f09f1640589c3", host="ec2-18-210-51-239.compute-1.amazonaws.com", port="5432", database="d5718s4db4oaif")

        cursor = connection.cursor()

        if continent == 'any' and type == 'any':
            return redirect('/generator')
            # redirect to main Generator
        elif continent != 'any' and type == 'any':
            cursor.execute("SELECT * FROM database WHERE continent = '{}' ORDER BY random()".format(continent))
            all_data = cursor.fetchone()
            try:
                place = all_data[1]
                google_link = link+place.replace(' ', '+')+" target='_blank'"
                google_it = "Google it!"
                info = "{} is located in {}. This is {} type of vacation.".format(all_data[1], all_data[3], all_data[4])
                description =  all_data[5]
                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            except:
                place = 'Sorry!'
                google_link = "/"
                google_it = "Go back"
                info = 'Could not find any place in this continent'
                description = 'No place like this in my database. Try another filter.'
                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            finally:
                cursor.close()


        elif continent == 'any' and type != 'any':
            cursor.execute("SELECT * FROM database WHERE type = '{}' ORDER BY random()".format(type))
            all_data = cursor.fetchone()
            try:
                place = all_data[1]
                google_link = link + place.replace(' ', '+')+" target='_blank'"
                google_it = "Google it!"
                info = "{} is located in {}. This is {} type of vacation.".format(all_data[1], all_data[3], all_data[4])
                description =  all_data[5]

                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            except:
                place = 'Sorry!'
                google_link = "/"
                google_it = "Go back"
                info = 'Could not find this type of vacation.'
                description = 'No place like this in my database. Try another filter.'
                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            finally:
                cursor.close()

        elif continent != 'any' and type != 'any':
            cursor.execute("SELECT * FROM database WHERE type = '{}' AND continent = '{}' ORDER BY random()".format(type, continent))

            try:

                all_data = cursor.fetchone()
                place = all_data[1]
                google_link = link + place.replace(' ', '+')+" target='_blank'"
                google_it = "Google it!"
                info = "{} is located in {}. This is {} type of vacation.".format(all_data[1], all_data[3], all_data[4])
                description =  all_data[5]

                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            except:

                place = 'Sorry!'
                google_link = "/"
                google_it = "Go back"
                info = 'Could not find this type of vacation in your selected continent'
                description = 'No place like this in my database. Try another filter.'
                return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)
            finally:
                cursor.close()

        else:
            place = 'Sorry!'
            info = ''
            google_link = "/"
            google_it = "Go back"
            description = 'No place like this in my database. Try another filter.'
            return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)

        place = 'Sorry!'
        info = ''
        google_link = "/"
        google_it = "Go back"
        description = 'No place like this in my database. Try another filter.'
        return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it)

@app.route('/generator', methods=['POST', 'GET'])
def generator():

    # connection = psycopg2.connect(user= "postgres", password = "berzone", host="localhost", port="5432", database="generator")

    connection = psycopg2.connect(user= "jynasdeissbqqu", password = "74d771fb1054684f37e31f1bf706d3d4c0afb39c8cd82a71120f09f1640589c3", host="ec2-18-210-51-239.compute-1.amazonaws.com", port="5432", database="d5718s4db4oaif")

    link = "https://www.google.com/search?q="
    map_link = "https://www.google.com/maps/place/"
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM database ORDER BY random()")
    all_data = cursor.fetchone()
    try:
        place = all_data[1]

        google_link = link+place.replace(' ', '+')+" target='_blank'"
        map = map_link+place.replace(' ', '+')+" target='_blank'"

        google_it = "Google it!"
        info = "{} is located in {}. This is {} type of vacation.".format(all_data[1], all_data[3], all_data[4])
        description =  all_data[5]
        cursor.close()
        return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it, map=map)
    except:
        place = 'Sorry!'
        info = ''
        google_link = "/"
        map = "/"
        google_it = "Try again!"
        description = 'No place like this in my database. Try another filter.'
        return render_template('destination.html', place=place, info=info, description=description, google_link=google_link, google_it=google_it, map=map)
    finally:
        cursor.close()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mail', methods=['POST', 'GET'])
def mail():
    print('works1')
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    send_mail(name, email, message)
    print('works2')
    return render_template('mail.html')


if __name__ == '__main__':
    app.run()
