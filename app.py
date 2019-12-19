from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
class User1(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = User1.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    user = User1.query.get_or_404(id)
    if request.method == 'POST':
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect('/')
    else:
        user1s = User1.query.all()
        page ='updatehome'
        return render_template('home.html',page=page,user1s=user1s,user=user)
@app.route('/',methods=['GET','POST'])
def get():
    if request.method == "GET":
        user1s = User1.query.all()
        page ='home'
        user = User1(firstname='',lastname='',email='',password='')
        return render_template('home.html',user1s=user1s,page=page,user=user)
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        newUser1 = User1(firstname=firstname,lastname=lastname,email=email,password=password)
        db.session.add(newUser1)
        db.session.commit()
        return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)