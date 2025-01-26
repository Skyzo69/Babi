import requests

# Ganti dengan token Discord milikmu
discord_token = 'MTEzNTExODc4NzUzMjgzMjgyOA.Gskvuf.C2ZCshajOm7jSLFEQgZUQlUGiN2ahQal2L6vSM'

# Endpoint untuk login menggunakan token (ini hanya contoh, pastikan untuk memeriksa dokumentasi API mereka)
login_url = 'https://app.drip.re/api/auth/discord'

# Headers untuk memberikan token Discord di permintaan
headers = {
    'Authorization': f'Bearer {discord_token}',
    'Content-Type': 'application/json'
}

# Kirim permintaan POST untuk login
response = requests.post(login_url, headers=headers)

# Cek apakah login berhasil
if response.status_code == 200:
    print('Login berhasil!')
    # Ambil data pengguna atau respons lain jika ada
    print(response.json())
else:
    print(f'Login gagal. Status code: {response.status_code}')
    print(response.text)
