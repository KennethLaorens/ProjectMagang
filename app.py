from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import requests
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Ganti dengan kunci rahasia

API_URL = 'https://api.sms-gateway-provider.com/send_sms'  # Ganti dengan URL API SMS Gateway
API_KEY = 'YOUR_API_KEY'  # Ganti dengan API Key Anda

def kirim_sms(nomor, pesan):
    data = {
        'to': nomor,
        'message': pesan,
        'api_key': API_KEY,
    }
    try:
        response = requests.post(API_URL, data=data)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Upload file Excel
        if 'file' not in request.files:
            flash('File belum diupload')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)

        filename = file.filename
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)

        # Baca data Excel
        df = pd.read_excel(filepath)
        columns = df.columns.tolist()
        # Simpan dataframe sementara di session atau file untuk proses lanjut

        return render_template('preview.html', columns=columns, filename=filename)

    return render_template('index.html')

@app.route('/send_sms', methods=['POST'])
def send_sms():
    filename = request.form.get('filename')
    kolom_nomor = request.form.get('kolom_nomor')
    kolom_pesan = request.form.get('kolom_pesan')

    filepath = os.path.join('uploads', filename)
    df = pd.read_excel(filepath)

    hasil = []
    for _, row in df.iterrows():
        nomor = str(row[kolom_nomor])
        pesan = str(row[kolom_pesan])
        res = kirim_sms(nomor, pesan)
        hasil.append({'nomor': nomor, 'pesan': pesan, 'status': res})

    return render_template('result.html', hasil=hasil)

if __name__ == '__main__':
    app.run(debug=True)
