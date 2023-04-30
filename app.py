#/**************************************************************************************************************************************************
#* File name     : flask CRUD demo
#* Compiler      : 
#* Author        : kito   
#* Created       : 2023/04/30
#* Modified      : 
#* Last modified : 2023/04/30
#*
#*
#* Description   : 
#*                  project to test and run python flask framework with some CRUD operation over SQLlite DB
#*
#* Other info    : 
#**************************************************************************************************************************************************/



from flask import Flask, abort,render_template,request,redirect
from models import db,EmployeeModel
 
app = Flask(__name__)
 
# DB connection and and init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# creation of the table, comment that if not first lunch on that pc
@app.route('/firstLunch' , methods = ['GET'])
def create_table():
    db.create_all()
    return redirect('/data')
 
# ROUTES

# /data
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position = position)
        # add in DB
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')
 
# LIST
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    print(employees)
    return render_template('dataList.html', employees = employees)
 
# DETAILS
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
        # error check
    return f"Employee with id ={id} doesn't exist"
 
# UPDATE
@app.route('/data/<int:id>/update', methods = ['GET','PUT'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'PUT':
        if employee:
            # remove from Db
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
            # add new version in DB
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        # error check
        return f"Employee with id = {id} Does nit exist"
 
    return render_template('update.html', employee = employee)
 
# DELETE
@app.route('/data/<int:id>/delete', methods=['GET','DELETE'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'DELETE':
        if employee:
            # delete from DB
            # db.session.delete(employee)
            # db.session.commit()
            return redirect('/data')
        abort(404)
 
    return render_template('delete.html')
 
# creation and start of web server
app.run(host='localhost', port=5000)