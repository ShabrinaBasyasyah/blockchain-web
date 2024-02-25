from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

user_data = {
    "Perusahaan ABC": {
        "username": "Perusahaan ABC",
        "idPerusahaan": "123",
        "password": "password"
    }
}

@app.route('/')
def login():
    return render_template('signin_signup.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    nama_perusahaan = request.form['nama_perusahaan']
    idPerusahaan = request.form['idPerusahaan']
    password = request.form['password']
    
    if nama_perusahaan in user_data:
        company_data = user_data[nama_perusahaan]
        if idPerusahaan == company_data['idPerusahaan'] and password == company_data['password']:
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('signup_failed'))

@app.route('/signup_failed')
def signup_failed():
    return render_template('signup_failed.html')

@app.route('/try_again', methods=['POST'])
def try_again():
    return redirect(url_for('login'))

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
