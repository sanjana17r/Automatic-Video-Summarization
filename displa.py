from flask import Flask, redirect, url_for, render_template,request

app = Flask(__name__)
@app.route("/",methods=['GET','POST'])  # this sets the route to this page
def home():
    if request.method=='POST':
        k=request.form['link']
        return redirect(url_for('index',ty=k))
    else:
        return render_template("index.html") # some basic inline html
@app.route("/index/<ty>",methods=['GET','POST'])  # this sets the route to this page
def index(ty):
    if request.method=='GET':
        print("got",ty)
    else:
        print("list(books['name.1'])")
if __name__ == "__main__":
    app.run(debug=True)
