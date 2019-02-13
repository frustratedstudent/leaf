from flask import Flask, url_for, request, render_template, g, redirect
import sqlite3

DATABASE = 'data/database.db'

app = Flask(__name__)


@app.route('/')
def action():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')
	
@app.route('/home', methods=["POST"])
def choice():

    if(request.form['choice']=='add'):
        return redirect(url_for('trip_form'))
    else:
        return redirect(url_for('map_year'))

		
@app.route('/add', methods=["GET"])
def trip_form():
	return render_template('trip_form.html')
	# return 'ok'

@app.route('/add', methods=["POST"])
def add_trip():

	conn = sqlite3.connect('data/database.db')
	
	cur = conn.cursor()
	
	cur.execute('SELECT country FROM cities WHERE city=?', [request.form['city']])
	
	country = cur.fetchone()[0]
	# north = cur.fetchone()[1]
	# east = cur.fetchone()[2]
	# print(country)
	
	cur.execute('INSERT INTO visits(country, city, year, img_link, comment) VALUES(?,?,?,?,?)',
				[country,request.form['city'],request.form['year'],request.form['img_link'],request.form['comment']])
				
	conn.commit()
	
	conn.close()
				
	return render_template('success.html')
	
@app.route('/map', methods=["GET"])
def map_year():
	return render_template('map_year.html')
	
@app.route('/map', methods=["POST"])
def show_map():

	conn = sqlite3.connect('data/database.db')
	
	cur = conn.cursor()
	
	cur.execute('SELECT * FROM visits WHERE year=?', [request.form['year']])
	
	rows = cur.fetchall();
	
	print(rows)
	
	return render_template('index.htm', rows = rows)

	
	
	
	
	

	
	

	
if __name__ == '__main__':
    app.run()