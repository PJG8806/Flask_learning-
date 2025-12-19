from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def user_list():
    item_list = [
        {"username": "traveler", "name": "Alex"},
        {"username": "photographer", "name": "Sam"},
        {"username": "gourmet", "name": "Chris"}
    ]
    user = "Chris"

    return render_template("index.html", item_list = item_list, user = user)

if __name__ == "__main__":
    app.run(debug=True)