from flask import Flask, render_template, request
import json
import webbrowser
import threading

app = Flask(__name__)

# ---------------- DATA LOADING ----------------
def load_data(filename):
    with open(filename, "r") as file:
        return json.load(file)

# ---------------- DATA CLEANING ----------------
def clean_data(data):
    # Remove users with empty names
    data["users"] = [u for u in data["users"] if u["name"].strip()]

    # Remove duplicate friends
    for u in data["users"]:
        u["friends"] = list(set(u["friends"]))

    # Keep valid users only
    data["users"] = [u for u in data["users"] if u["friends"] or u["liked_pages"]]

    # Remove duplicate pages
    page_map = {}
    for p in data["pages"]:
        page_map[p["id"]] = p
    data["pages"] = list(page_map.values())

    return data

# ---------------- PEOPLE RECOMMENDATION ----------------
def find_people_you_may_know(user_id, data):
    friends_map = {}
    id_name_map = {}

    for u in data["users"]:
        friends_map[u["id"]] = set(u["friends"])
        id_name_map[u["id"]] = u["name"]

    if user_id not in friends_map:
        return []

    direct = friends_map[user_id]
    suggestions = {}

    for friend in direct:
        for mutual in friends_map[friend]:
            if mutual != user_id and mutual not in direct:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    ordered = sorted(suggestions, key=suggestions.get, reverse=True)
    return [id_name_map[i] for i in ordered]

# ---------------- PAGE RECOMMENDATION ----------------
def find_pages_you_might_like(user_id, data):
    user_page_map = {}
    page_name_map = {}

    for u in data["users"]:
        user_page_map[u["id"]] = set(u["liked_pages"])

    for p in data["pages"]:
        page_name_map[p["id"]] = p["name"]

    if user_id not in user_page_map:
        return []

    liked = user_page_map[user_id]
    suggestions = {}

    for other_id, pages in user_page_map.items():
        if other_id != user_id:
            common = liked.intersection(pages)

            if len(common) > 0:
                for page in pages:
                    if page not in liked:
                        suggestions[page] = suggestions.get(page, 0) + len(common)

    ordered = sorted(suggestions, key=suggestions.get, reverse=True)
    return [page_name_map[i] for i in ordered]

# ---------------- LOAD DATA ----------------
data = clean_data(load_data("codebook.json"))

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    people = []
    pages = []
    error = None

    if request.method == "POST":
        try:
            user_id = int(request.form["user_id"])

            valid_ids = [u["id"] for u in data["users"]]

            if user_id not in valid_ids:
                error = "User ID not found ❌"
            else:
                people = find_people_you_may_know(user_id, data)
                pages = find_pages_you_might_like(user_id, data)

        except:
            error = "Invalid input ❌"

    return render_template("index.html", people=people, pages=pages, error=error)

# ---------------- AUTO OPEN BROWSER ----------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)