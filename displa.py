from flask import Flask, redirect, url_for, render_template,request
from summarizer import summarize as s

app = Flask(__name__)
@app.route("/",methods=['GET','POST'])  # this sets the route to this page
def home():
    if request.method=='POST':
        link=request.form['link']
        return redirect(url_for('index',link=link))
    else:
        return render_template("index.html") # some basic inline html
@app.route("/index/<link>",methods=['GET','POST'])  # this sets the route to this page
def index(link):
    if request.method=='GET':
        print("Got link ",link)
        s.summarizer(link,2)
        return render_template("video.html")
    else:
        return render_template("video.html") # some basic inline html
if __name__ == "__main__":
    app.run(debug=True)
