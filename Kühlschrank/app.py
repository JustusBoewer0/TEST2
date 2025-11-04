from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "mega-geheimes-passwort"  # für Sessions
app.jinja_env.globals.update(enumerate=enumerate)

DATEI = "produkte.json"
USER_DATEI = "users.json"

# ------------------ PRODUKTE LADEN ------------------
def lade_produkte():
    if os.path.exists(DATEI):
        with open(DATEI, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    return {}

def speichere_produkte(produkte):
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(produkte, f, ensure_ascii=False, indent=2)

produkte = lade_produkte()

# ------------------ BENUTZER LADEN ------------------
def lade_users():
    if os.path.exists(USER_DATEI):
        with open(USER_DATEI, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    return {"admin": "admin"}  # Standard-Admin

def speichere_users(users):
    with open(USER_DATEI, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users = lade_users()

# ------------------ PRODUKTNAME über Barcode ------------------
def get_produktname(barcode):
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("product", {}).get("product_name", "").strip()
    except:
        pass
    return None

# ------------------ ROUTE ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    global users

    # LOGIN
    if "user" not in session:
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            if username in users and users[username] == password:
                session["user"] = username
                if username not in produkte:
                    produkte[username] = []
                    speichere_produkte(produkte)
                return redirect(url_for("index"))
            else:
                error = "Falscher Login"
        return render_template("index.html", login=True, error=error)

    # BENUTZER EINGELOGGT
    user = session["user"]
    if user not in produkte:
        produkte[user] = []

    dev_mode = user == "admin"  # Admin kann Benutzer bearbeiten

    # ADMIN-FUNKTION: Benutzer hinzufügen/löschen
    if dev_mode and request.method == "POST":
        if "add_user" in request.form:
            new_user = request.form.get("new_user").strip()
            new_pass = request.form.get("new_pass").strip()
            if new_user and new_pass:
                users[new_user] = new_pass
                speichere_users(users)
        elif "delete_user" in request.form:
            del_user = request.form.get("delete_user")
            if del_user in users and del_user != "admin":
                users.pop(del_user)
                speichere_users(users)

    # PRODUKT-HANDLING
    if request.method == "POST" and not request.form.get("username"):
        if "add" in request.form:
            barcode = request.form.get("barcode", "").strip()
            manual_name = request.form.get("manual_name", "").strip()
            ablauf = request.form.get("ablauf", "").strip()
            if manual_name:
                name = manual_name
            elif barcode:
                name = get_produktname(barcode) or f"Unbekanntes Produkt ({barcode})"
            else:
                name = "Unbekanntes Produkt"
            produkte[user].append({"name": name, "ablauf": ablauf})
            speichere_produkte(produkte)

        elif "delete" in request.form:
            index_to_delete = int(request.form.get("delete"))
            if 0 <= index_to_delete < len(produkte[user]):
                produkte[user].pop(index_to_delete)
                speichere_produkte(produkte)

        elif "edit" in request.form:
            index_to_edit = int(request.form.get("edit_index"))
            neuer_name = request.form.get("edit_name", "").strip()
            if 0 <= index_to_edit < len(produkte[user]) and neuer_name:
                produkte[user][index_to_edit]["name"] = neuer_name
                speichere_produkte(produkte)

        return redirect(url_for("index"))

    # PRODUKTSUCHE
    suchbegriff = request.args.get("suche", "").strip().lower()
    gefiltert = produkte[user]
    if suchbegriff:
        gefiltert = [p for p in produkte[user] if suchbegriff in p["name"].lower()]

    return render_template("index.html", produkte=gefiltert, user=user, login=False, dev_mode=dev_mode, users=users)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)