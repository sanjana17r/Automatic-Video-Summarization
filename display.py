from flask import Flask, redirect, url_for, render_template,request
from summarizer import summarize

app = Flask(__name__)
@app.route("/",methods=['GET','POST'])  # this sets the route to this page
def home():
    if request.method=='POST':
        link=request.form['link']
        time = request.form['time']
        video_id = link[-11:]
        time=int(time)
        return redirect(url_for('index',link=video_id,time=time))
    else:
        return render_template("index.html") # some basic inline html
@app.route("/index/<link>/<time>",methods=['GET','POST'])  # this sets the route to this page
def index(link,time):
    link = "https://www.youtube.com/watch?v="+link
    if request.method=='GET':
        print("Got link ",link)
        print("Got time ",time)
        summarize(link,time)
        return render_template("video.html")
    else:
        return render_template("video.html") # some basic inline html
if __name__ == "__main__":
    app.run(debug=True)
