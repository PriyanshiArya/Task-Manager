from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    rating = db.Column(db.Integer , nullable = False)

    def __repr__(self):
        return '<Task %x>' %self.id

@app.route('/' , methods = ['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        task_rating = request.form['rating']
        new_task= Todo(content = task_content, rating=task_rating)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html' , tasks = tasks)

@app.route('/delete/<int:i>')
def delete(i):
    task_to_delete = Todo.query.get_or_404(i)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"    

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method =='POST':
        task.content = request.form['content']
        task.rating = request.form['rating']


        try:
           db.session.commit() 
           return redirect('/')
        except:
            return'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)    

