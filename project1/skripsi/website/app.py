from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

user_data = {
    "username" : "Perusahaan ABC",
    "nama_perusahaan": "Perusahaan ABC",
    "idPerusahaan": "123",
    "password": "password"
}

@app.route('/')
def login():
    return render_template('signin_signup.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    nama_perusahaan = request.form['nama_perusahaan']
    idPerusahaan = request.form['idPerusahaan']
    password = request.form['password']
    if nama_perusahaan == user_data['nama_perusahaan'] and idPerusahaan == user_data['idPerusahaan'] and password == user_data['password']:
        return redirect(url_for('dashboard'))
    else: 
        return redirect(url_for('login'))
    
@app.route ('/dashboard')
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