from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import json
import os
import random

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


# ------------------ KI REZEPT GENERATOR ------------------
def generiere_rezept(produkte_liste):
    """
    Generiert ein kreatives Rezept basierend auf den verfügbaren Produkten.
    Verwendet ein intelligentes Template-System für realistische Rezepte.
    """
    if not produkte_liste or len(produkte_liste) == 0:
        return None

    # Extrahiere nur die Produktnamen
    produkt_namen = [p["name"].lower() for p in produkte_liste]

    # Kategorisiere Produkte
    kategorien = {
        "gemüse": ["tomate", "gurke", "paprika", "zwiebel", "knoblauch", "karotte", "salat", "spinat", "brokkoli", "zucchini", "aubergine"],
        "fleisch": ["hähnchen", "hühnchen", "chicken", "rind", "schwein", "hackfleisch", "wurst", "schinken", "speck"],
        "fisch": ["lachs", "thunfisch", "forelle", "garnele", "fisch"],
        "milchprodukte": ["milch", "käse", "butter", "sahne", "joghurt", "quark", "mozzarella", "parmesan"],
        "kohlenhydrate": ["nudeln", "pasta", "reis", "kartoffel", "brot", "brötchen"],
        "gewürze": ["salz", "pfeffer", "paprika", "curry", "oregano", "basilikum", "petersilie"],
        "obst": ["apfel", "banane", "erdbeere", "orange", "zitrone", "kirsche", "traube"]
    }

    # Finde passende Kategorien
    gefundene_kategorien = set()
    for produkt in produkt_namen:
        for kategorie, keywords in kategorien.items():
            if any(keyword in produkt for keyword in keywords):
                gefundene_kategorien.add(kategorie)

    # Rezept-Templates basierend auf verfügbaren Zutaten
    rezept_templates = []

    # Pasta-Rezepte
    if "kohlenhydrate" in gefundene_kategorien or any("nudel" in p or "pasta" in p for p in produkt_namen):
        rezept_templates.append({
            "title": "Cremige Pasta mit frischen Zutaten",
            "description": "Ein schnelles und leckeres Pasta-Gericht mit Zutaten aus deinem Kühlschrank",
            "base_ingredients": ["Pasta oder Nudeln", "Olivenöl", "Salz & Pfeffer"],
            "time": "ca. 20-25 Minuten",
            "servings": "2 Personen",
            "steps": [
                "Einen großen Topf mit Salzwasser zum Kochen bringen",
                "Die Nudeln nach Packungsanleitung al dente kochen",
                "In der Zwischenzeit die zusätzlichen Zutaten vorbereiten und in einer Pfanne mit Olivenöl anbraten",
                "Die gekochten Nudeln abgießen und zur Pfanne geben",
                "Alles gut vermengen und mit Salz und Pfeffer abschmecken",
                "Heiß servieren und nach Belieben mit Parmesan garnieren"
            ]
        })

    # Salat-Rezepte
    if "gemüse" in gefundene_kategorien:
        rezept_templates.append({
            "title": "Frischer Kühlschrank-Salat",
            "description": "Ein knackiger, gesunder Salat mit allem, was dein Kühlschrank hergibt",
            "base_ingredients": ["Frisches Gemüse", "Olivenöl", "Essig oder Zitrone"],
            "time": "ca. 15 Minuten",
            "servings": "2 Personen",
            "steps": [
                "Das Gemüse gründlich waschen und in mundgerechte Stücke schneiden",
                "Alles in einer großen Schüssel vermengen",
                "Ein einfaches Dressing aus Olivenöl, Essig, Salz und Pfeffer zubereiten",
                "Das Dressing über den Salat geben und gut durchmischen",
                "Optional: Mit Nüssen, Käse oder Croutons toppen",
                "Sofort servieren und genießen"
            ]
        })

    # Pfannengericht
    if "fleisch" in gefundene_kategorien or "gemüse" in gefundene_kategorien:
        rezept_templates.append({
            "title": "Buntes Pfannengericht",
            "description": "Ein herzhaftes One-Pan-Gericht mit proteinreichen Zutaten und Gemüse",
            "base_ingredients": ["Protein deiner Wahl", "Gemüse", "Gewürze"],
            "time": "ca. 30 Minuten",
            "servings": "2-3 Personen",
            "steps": [
                "Die Hauptzutaten in mundgerechte Stücke schneiden",
                "Eine große Pfanne mit etwas Öl erhitzen",
                "Zuerst das Protein scharf anbraten, bis es goldbraun ist",
                "Das Gemüse hinzufügen und unter Rühren weiterbraten",
                "Mit deinen Lieblingsgewürzen würzen und abschmecken",
                "Bei mittlerer Hitze fertig garen bis alles durch ist",
                "Mit Reis, Nudeln oder Brot servieren"
            ]
        })

    # Omelette/Frühstück
    if "milchprodukte" in gefundene_kategorien:
        rezept_templates.append({
            "title": "Gefülltes Omelette",
            "description": "Ein protein-reiches Omelette gefüllt mit frischen Zutaten",
            "base_ingredients": ["3-4 Eier", "Butter oder Öl", "Salz & Pfeffer"],
            "time": "ca. 10-15 Minuten",
            "servings": "1-2 Personen",
            "steps": [
                "Die Eier in einer Schüssel verquirlen und mit Salz und Pfeffer würzen",
                "Eine Pfanne bei mittlerer Hitze erhitzen und Butter oder Öl hineingeben",
                "Die Eiermischung in die Pfanne gießen und gleichmäßig verteilen",
                "Die Füllung (Gemüse, Käse, etc.) auf einer Hälfte des Omeletts verteilen",
                "Wenn die Unterseite gestockt ist, das Omelette vorsichtig zusammenklappen",
                "Noch 1-2 Minuten braten lassen, dann auf einen Teller gleiten lassen",
                "Mit frischen Kräutern garnieren und sofort servieren"
            ]
        })

    # Suppe
    rezept_templates.append({
        "title": "Hausgemachte Kühlschrank-Suppe",
        "description": "Eine wärmende, nahrhafte Suppe aus übrig gebliebenen Zutaten",
        "base_ingredients": ["Gemüsebrühe oder Wasser", "Zwiebeln", "Gewürze"],
        "time": "ca. 35-40 Minuten",
        "servings": "3-4 Personen",
        "steps": [
            "Zwiebeln und Knoblauch fein hacken und in einem Topf mit Öl anschwitzen",
            "Härteres Gemüse hinzufügen und kurz mitbraten",
            "Mit Brühe oder Wasser aufgießen und zum Kochen bringen",
            "Weicheres Gemüse und weitere Zutaten hinzufügen",
            "Bei mittlerer Hitze 20-25 Minuten köcheln lassen",
            "Mit Salz, Pfeffer und Gewürzen nach Geschmack abschmecken",
            "Optional: Mit einem Stabmixer pürieren oder stückig lassen",
            "Mit frischem Brot servieren"
            ]
        })

    # Wähle ein passendes Rezept oder das letzte als Fallback
    if not rezept_templates:
        rezept_templates.append({
            "title": "Kreative Kühlschrank-Verwertung",
            "description": "Ein improvisiertes Gericht mit deinen verfügbaren Zutaten",
            "base_ingredients": ["Deine verfügbaren Produkte", "Öl zum Braten", "Gewürze"],
            "time": "ca. 25-30 Minuten",
            "servings": "2 Personen",
            "steps": [
                "Alle verfügbaren Zutaten waschen und vorbereiten",
                "Eine Pfanne mit Öl erhitzen",
                "Die Zutaten der Reihe nach hinzufügen - erst härtere, dann weichere",
                "Unter regelmäßigem Rühren garen",
                "Kreativ mit Gewürzen abschmecken",
                "Wenn alles gar ist, auf Tellern anrichten und genießen"
            ]
        })

    # Wähle zufälliges Rezept
    rezept = random.choice(rezept_templates)

    # Füge die echten Produkte zu den Zutaten hinzu
    echte_zutaten = [p["name"] for p in produkte_liste[:8]]  # Max 8 Produkte
    alle_zutaten = rezept["base_ingredients"] + echte_zutaten

    # Entferne Duplikate und behalte Reihenfolge
    seen = set()
    unique_zutaten = []
    for zutat in alle_zutaten:
        zutat_lower = zutat.lower()
        if zutat_lower not in seen:
            seen.add(zutat_lower)
            unique_zutaten.append(zutat)

    rezept["ingredients"] = unique_zutaten

    return rezept


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

    return render_template(
        "index.html",
        produkte=gefiltert,
        user=user,
        login=False,
        dev_mode=dev_mode,
        users=users,
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/api/generate-recipe")
def api_generate_recipe():
    """API Endpunkt zum Generieren von Rezepten basierend auf Benutzerprodukten"""
    if "user" not in session:
        return jsonify({"success": False, "message": "Nicht eingeloggt"}), 401

    user = session["user"]
    if user not in produkte or len(produkte[user]) == 0:
        return jsonify({
            "success": False,
            "message": "Du hast noch keine Produkte in deinem Kühlschrank! Füge erst einige Produkte hinzu."
        })

    rezept = generiere_rezept(produkte[user])

    if rezept:
        return jsonify({"success": True, "recipe": rezept})
    else:
        return jsonify({
            "success": False,
            "message": "Rezeptgenerierung fehlgeschlagen. Bitte versuche es erneut."
        })


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
