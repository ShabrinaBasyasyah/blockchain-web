from flask import Flask, render_template, request, redirect, url_for
import psycopg2
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

def authenticate_signup(nama_perusahaan):
    company_data = get_company_info(nama_perusahaan)
    if company_data:
        company_id = company_data[0]
        company_name = company_data[1]
        return company_id, company_name
    return None, None

def save_user_data(id_perusahaan, username, password):
    # Generate hashed password
    
    # Simpan data pengguna ke dalam tabel users
    conn = psycopg2.connect(
        dbname="ptbae",
        user="postgres",
        password="dks120193",
        host="localhost",
        port=5433
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id_perusahaan, username, password) VALUES (%s, %s, %s)", (id_perusahaan, username, password))
    conn.commit()
    cur.close()
    conn.close()



def authenticate_signin(id_perusahaan, username, password):
    conn = psycopg2.connect(
        dbname="ptbae",
        user="postgres",
        password="dks120193",
        host="localhost",
        port=5433
    )
    cur = conn.cursor()
    cur.execute("SELECT id_perusahaan, username, password FROM users WHERE id_perusahaan = %s AND username = %s", (id_perusahaan, username,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
      
    if user_data:
        stored_id_perusahaan, stored_username, stored_password = user_data
        # Decode the hashed password from the database before comparing
        if id_perusahaan == stored_id_perusahaan and username == stored_username and  password==stored_password:
            return True
    return False

# Route untuk halaman utama
@app.route('/')
def landing():
    return render_template('landingpage.html')

# Route untuk halaman sign up
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route untuk autentikasi sign up
@app.route('/signup/authenticate', methods=['POST'])
def authenticate_signup_route():
    nama_perusahaan = request.form['nama_perusahaan']
    id_perusahaan, nama_perusahaan = authenticate_signup(nama_perusahaan)
    if id_perusahaan and nama_perusahaan:
        # Peroleh username dan password yang diinput oleh pengguna
        username = request.form['username']
        password = generate_password()
        # Simpan data pengguna ke dalam tabel users
        save_user_data(id_perusahaan, username, password)
        # Redirect ke halaman berhasil sign up
        return render_template('signup_berhasil.html', company_id=id_perusahaan, company_name=nama_perusahaan, password=password)
    else:
        return redirect(url_for('signup_failed'))

# Route untuk halaman sign up gagal
@app.route('/signup_failed')
def signup_failed():
    return render_template('signup_failed.html')

# Route untuk mencoba lagi
@app.route('/try_again', methods=['POST'])
def try_again():
    return redirect(url_for('login'))

# Route untuk halaman login
@app.route('/login')
def login():
    return render_template('signin.html')

# Route untuk autentikasi sign in
@app.route('/signin/authenticate', methods=['POST'])
def authenticate_signin_route():
    username = request.form['username']
    password = request.form['password']  # Get the password directly from the form
    id_perusahaan = request.form['id_perusahaan']
    if authenticate_signin(id_perusahaan, username, password):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login_failed'))
    
# Route untuk halaman login gagal
@app.route('/login_failed')
def login_failed():
    return render_template('signin_failed.html')

# Route untuk dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route untuk halaman home
@app.route('/home')
def home():
    return render_template('dashboard.html')

# Route untuk membuat permintaan
@app.route('/create_permintaan')
def buat_permintaan():
    return render_template('create_permintaan.html')

# Route untuk membuat penawaran
@app.route('/create_penawaran')
def buat_penawaran():
    return render_template('create_penawaran.html')

# Route untuk transaksi beli
@app.route('/transaksibeli')
def buattransaksibeli():
    return render_template('transaksibeli.html')

# Route untuk transaksi jual
@app.route('/transaksijual')
def buattransaksijual():
    return render_template('transaksijual.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
