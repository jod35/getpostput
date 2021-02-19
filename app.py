from flask import Flask, json,make_response,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os
from marshmallow import Schema,fields



BASE_DIR=os.path.dirname(os.path.realpath(__file__))


app=Flask(__name__)


#configure database location
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(BASE_DIR,'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app) #configure sqlalchemy to work with app


#database model
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),nullable=False)
    course=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Student <{self.username}> <course {self.course}>"

#to create the db with such structure, run db.create_all()

#serializer 
class StudentSchema(Schema):
    id=fields.Integer()
    username=fields.String()
    course=fields.String()

@app.route('/',methods=["GET"])
def index():
    return jsonify({"message":"Hello"})

@app.route('/students',methods=["GET"])
def get_all_students():
    students=Student.query.all()

    data=StudentSchema(many=True).dump(students)
    return jsonify({"students":data})


@app.route('/student/<int:id>',methods=["GET"])
def get_one_student(id):
    student=Student.query.get_or_404(id)
    data=StudentSchema().dump(student)

    return jsonify({"student":data})


@app.route('/students',methods=["POST"])
def create_new_student():
    data=request.get_json()

    #create a student witn attr from the client
    new_stu=Student(username=data.get('username'),course=data.get('course'))

    db.session.add(new_stu)
    #saving the data to db
    db.session.commit()

    data=StudentSchema().dump(new_stu)

    return make_response(jsonify({"message":"Created","student":data}))


@app.route('/student/update/<int:id>',methods=["PUT"])
def update_student(id):
    data=request.get_json()

    student=Student.query.get_or_404(id)

    student.username=data.get("username")

    student.course=data.get("course")

    db.session.commit()

    data=StudentSchema().dump(student)

    return make_response(jsonify({"message":"Updated successfully","student":data}))



    
@app.route('/student/delete/<int:id>')
def delete(id):
	student=Student.query.get_or_404(id)
	
	db.session.delete(student)
	
	db.session.commit()

	return make_response(jsonify({"message":"Resource Deleted"}))




if __name__ == "__main__":
    app.run(debug=True)
