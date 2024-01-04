# import library third party
from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
# init main app
app = Flask(__name__)
app.secret_key = '!@#$%'
# databese comfig
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='webp1'
# init mysql
mysql = MySQL(app)
# set route default
@app.route('/', methods=['GET','POST'])
def login():
    #cek jika methods POST dan ada form data maka proses login
    if request.method == 'POST' and 'inpuser' in request.form and 'inpPass' in request.form:
        #buat variabel untuk memudahkan pengolahan data
        username = request.form['inpuser']
        passwd = request.form['inpPass']
        #cursor koneksi mysql
        cur = mysql.connection.cursor()
        #eksekusi kueri
        cur.execute("SELECT * FROM data where username = %s and password= %s", (username, passwd))
        #fetch hasil
        result = cur.fetchone()
        #cek hasil kueri
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/home')
# function home
def home():
    if 'is_logged_in' in session:
        #cursor koneksi mysql
        cur = mysql.connection.cursor()
        #eksekusi kueri
        cur.execute("SELECT * FROM data")
        #fetch hasil kueri masukkan ke var data
        data = cur.fetchall()
        #tutup koneksi
        cur.close()
        #render array data sebagai users bersama bersama template
        return render_template('home.html', users=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#debug dan auto reload
if __name__ == '__main__':
    app.run(debug=True)
