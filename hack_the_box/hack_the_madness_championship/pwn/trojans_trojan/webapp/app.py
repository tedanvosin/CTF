from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from base64 import b64decode, b64encode
import binascii

DATABASE = os.path.join(os.getcwd(), "notes.db")
EXTENSION = os.path.join(os.getcwd(), "ext")

app = Flask(__name__)

db = None
def get_db():
    global db

    if db == None:
        db = sqlite3.connect(DATABASE)
        db.enable_load_extension(True)
        db.load_extension(EXTENSION)
        db.enable_load_extension(False)
    
    return db

def cache_select(title):
    if title == None: return
    return get_db().cursor().execute("SELECT HEX(note_cache(?))", (title, )).fetchone()[0]

def select_all():
    notes = get_db().cursor().execute("SELECT * FROM notes").fetchall()
    for i in range(len(notes)):
        notes[i] = (notes[i][0], b64encode(notes[i][1]).decode(), b64encode(notes[i][2]).decode())
    return notes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_all")
def get_all():
    return jsonify(select_all())

@app.route("/get", methods=["GET", "POST"])
def get_one():
    title = request.values.get("title")
    if title == None:
        return "Missing title", 400

    try:
        title = b64decode(title)
    except binascii.Error:
        return "Invalid base64", 400

    result = cache_select(title)
    if result:
        return b64encode(bytes.fromhex(result))

    return f"Note with title '{title}' does not exist", 400

@app.route("/delete", methods=["GET", "POST"])
def delete():
    title = request.values.get("title")
    if title == None:
        return "Missing title", 400

    try:
        title = b64decode(title)
    except binascii.Error:
        return "Invalid base64", 400
    
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM notes WHERE title=?", (title, ))
    db.commit()

    if cur.rowcount == 0:
        return f"Note with title '{title}' does not exist", 400

    return "Success"

@app.route("/create", methods=["GET", "POST"])
def create():
    title = request.values.get("title")
    if title == None:
        return "Missing title", 400

    content = request.values.get("content")
    if content == None:
        return "Missing content", 400

    try:
        title = b64decode(title)
        content = b64decode(content)
    except binascii.Error:
        return "Invalid base64", 400

    if cache_select(title):
        return f"Note with title '{title}' already exists", 400

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    db.commit()

    if cur.rowcount == 0:
        return "Something went wrong", 500

    return "Success"

@app.route("/change", methods=["GET", "POST"])
def change():
    old_title = request.values.get("old_title")
    if old_title == None:
        return "Missing old_title", 400

    new_title = request.values.get("new_title")
    if new_title == None:
        return "Missing new_title", 400

    new_content = request.values.get("new_content")
    if new_content == None:
        return "Missing new_content", 400

    try:
        old_title = b64decode(old_title)
        new_title = b64decode(new_title)
        new_content = b64decode(new_content)
    except binascii.Error:
        return "Invalid base64", 400

    if new_title != old_title and cache_select(new_title):
        return f"Note with title '{new_title}' already exists", 400

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE notes SET title=?, content=? WHERE title=?", (new_title, new_content, old_title))
    db.commit()

    if cur.rowcount == 0:
        return "Something went wrong", 500

    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, threaded=False)
