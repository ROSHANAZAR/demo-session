from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        user_name=request.form['name']
        new_task=users(name=user_name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "something went wrong"
    else:
        tasks=users.query.all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=users.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "something went wrong"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=users.query.get_or_404(id)

    if request.method=='POST':
        task.name=request.form['name']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "something went wrong"

    else:
        return render_template('update.html',task=task)

if __name__=="__main__":
    app.run(host="0.0.0.0" ,debug=True)


