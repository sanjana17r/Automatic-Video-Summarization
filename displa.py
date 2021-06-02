from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
@app.route("/")  # this sets the route to this page
def home():
	return render_template("index.html") # some basic inline html
if __name__ == "__main__":
    app.run(debug=True)