from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import bcrypt
import random
import string

app = Flask(__name__)

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(8))
    return password

def get_company_info(nama_perusahaan):
    conn = psycopg2.connect(
        dbname="ptbae",
        user="postgres",
        password="dks120193",
        host="localhost",
        port=5433
    )
    cur = conn.cursor()
    cur.execute("SELECT id_perusahaan, nama_perusahaan FROM perusahaan WHERE nama_perusahaan = %s", (nama_perusahaan,))
    company_data = cur.fetchone()
    cur.close()
    conn.close()
    return company_data

@app.route('/')
def landing():
    return render_template('landingpage.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    nama_perusahaan = request.form['nama_perusahaan']
    
    company_data = get_company_info(nama_perusahaan)
    if company_data:
        company_id = company_data[0]  # Mendapatkan company_id dari indeks 0
        company_name = company_data[1]  # Mendapatkan company_name dari indeks 1
        return render_template('signup_berhasil.html', company_id=company_id, company_name=company_name, password=generate_password())
    
    # Jika perusahaan tidak ditemukan, arahkan pengguna ke halaman sign up failed
    return redirect(url_for('signup_failed'))
    
@app.route('/signup_failed')
def signup_failed():
    return render_template('signup_failed.html')

@app.route('/try_again', methods=['POST'])
def try_again():
    return redirect(url_for('login'))



@app.route('/login')
def login():
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/home')
def home():
    return render_template('dashboard.html')

@app.route('/create_permintaan')
def buat_permintaan():
    return render_template('create_permintaan.html')

@app.route('/create_penawaran')
def buat_penawaran():
    return render_template('create_penawaran.html')

@app.route('/transaksibeli')
def buattransaksibeli():
    return render_template('transaksibeli.html')

@app.route('/transaksijual')
def buattransaksijual():
    return render_template('transaksijual.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
