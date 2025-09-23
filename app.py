from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str: 
       return f"{self.sno} - {self.tittle} - {self.desc} - {self.date_created}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/" , methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        tittle = request.form['tittle']
        desc = request.form['desc']
        todo = Todo(tittle=tittle, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        tittle = request.form['tittle']
        desc = request.form['desc']
        todo.tittle = tittle
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        allTodo = Todo.query.all()
        print(allTodo)
    app.run(debug=True)