from flask import Flask , render_template , redirect , session , request , flash
import sqlite3 
import os 





app = Flask(__name__)
app.secret_key = 'Nyla_application'
app.config['UPLOAD_DOCUMENT'] = 'static/documents'

##
# home page d'accueil
#
#
@app.route('/')
@app.route('/home')
def home():
    return render_template('front/index.html')

#
# Porfolio 
# 
@app.route('/portfolio')
def portfolio():
    return render_template('front/portfolio.html')    


## 
# cote back-end 
#
# 
@app.route("/login",methods = ['GET','POST']) 
def login():
    if request.method == 'POST':
        user = request.form['user']
        pwd  = request.form['pwd'] 

        with sqlite3.connect("nila.db") as con :
            cur = con.cursor()
            cur.execute("select * from users where fullNames = ?  and passwordUser = ?", [user,pwd])
            data = cur.fetchone()

            if data:
                session['okey'] = True 
                session['id']  = data[0]
                session['fullname'] = data[1] 
                session['function'] = data[2] 

                return redirect('/admin')
            else:
                flash("mot de passe incorrecte".capitalize())
    return render_template('back/page-login.html')
##
#
# Admin 
#
@app.route('/admin')
def admin():
    if 'okey' in session :
        return render_template('back/index.html')
    else:
        return redirect('/login')
    
##
#
# deconnexion 
#
@app.route('/deco')
def deco():
    session.clear()
    
    return redirect('/')


##
#
# creation du compte  professeur 
@app.route("/register",methods = ['POST','GET']) 
def register():
    if request.method == 'POST':
        user = request.form['user']
        post = request.form['postnom']  
        phone= request.form['phone']
        role = 'formateur'
        pwd  = request.form['pwd']
        pwd2 = request.form['pwd2'] 

        # verification du double mot de passe 
        if pwd == pwd2:
            with sqlite3.connect("nila.db") as con :
                cur = con.cursor()
                cur.execute("insert into users(fullNames,passwordUser,phoneUser,postNom, fuctionUser) values(?,?,?,?,?)",[user,pwd,phone,post,role])
                con.commit()
                return redirect('/login')
        else:
            flash("les mot de passe doivent etre identique")
    return render_template('back/page-register.html')
#
#
# add professeur 
@app.route("/addP", methods = ['POST','GET'])
def addP():
    if request.method == 'POST':
        name  = request.form['username']
        fis   = request.form['prenom'] 
        phone = request.form['phone']
        valpassword = request.form['valpassword'] 
        confirmpassword = request.form['valconfirmpassword'] 

        if valpassword == confirmpassword:
            with sqlite3.connect("nila.db") as con :
                cur = con.cursor()
                cur.execute("insert into users(fullNames,phoneUser,postNom,fuctionUser,passwordUser) values(?,?,?,?,?)", [name,phone,fis,'professeur',valpassword])
                con.commit()
                flash("information enregistre !!!")
        else:
            flash("le mot de passe doit etre conforme")




    return render_template('back/form-validation.html')

##
#
# creation du compte  student
@app.route("/user",methods = ['POST','GET']) 
def user():
    if request.method == 'POST':
        user = request.form['user']
        post = request.form['postnom']  
        phone= request.form['phone']
        role = 'apprenant'
        pwd  = request.form['pwd']
        pwd2 = request.form['pwd2'] 

        # verification du double mot de passe 
        if pwd == pwd2:
            with sqlite3.connect("nila.db") as con :
                cur = con.cursor()
                cur.execute("insert into users(fullNames,passwordUser,phoneUser,postNom, fuctionUser) values(?,?,?,?,?)",[user,pwd,phone,post,role])
                con.commit()
                return redirect('/login')
        else:
            flash("les mot de passe doivent etre identique")
    return render_template('back/blank.html')

#
#
# messagerie liste
#
#
@app.route('/message', methods = ['GET','POST']) 
def message():
    if 'okey' in session:
        with sqlite3.connect('nila.db') as con :
            cur = con.cursor()
            cur.execute("select * from messages") 
            data = cur.fetchall()

        return render_template('back/email-inbox.html', data = data) 

#
#
# Module 
@app.route('/module', methods = ['GET','POST'] )
def module():
    if 'okey' in session:
        if request.method == 'POST':
            module = request.form['module']

            #verification si le module existe deja 
            with sqlite3.connect("nila.db") as con :
                ver = con.cursor()
                ver.execute("select * from modules  where libelleModule = ? ",[module])
                dataV = ver.fetchone()
                
                if dataV :
                    flash("le module existe deja dans la base de donnee")
                else :
                    cur = con.cursor()
                    cur.execute("insert into modules(libelleModule) values(?)",[module]) 
                    con.commit()
                    cur.close()
                    flash(f" {module} a etes ajouter avec succes")  
        return render_template('back/form-step.html')

    else:
        return redirect('/login')
#
# liste de module 
@app.route("/listM" , methods = ['POST','GET'])
def listM():
    if 'okey' in session:
        with sqlite3.connect("nila.db") as con :
            cur = con.cursor()
            cur.execute("select * from modules")
            aff = cur.fetchall()

        return render_template('back/table-datatable.html' , aff = aff) 
    else:
        return redirect('/login') 
    
#
#
# compose email-compose.html
@app.route('/compose',methods = ['POST','GET'])
def compose():
    if 'okey' in session:
        if request.method == 'POST' :
            des = request.form['des']
            exp = session['id'] 
            sub = request.form['Subject'] 
            tex = request.form['text'] 
            doc = request.files['file']

            file = os.path.join(app.config['UPLOAD_DOCUMENT'],doc.filename) 
            doc.save(file) 

            with sqlite3.connect("nila.db") as con :
                cur = con.cursor()
                cur.execute("insert into messages(expM,dexM,sujetM,message,document) values(?,?,?,?,?)",[exp,des,sub,tex,doc.filename])
                con.commit()
                flash("message expediee !!!")
        with sqlite3.connect("nila.db") as con :
            cur = con.cursor()
            cur.execute("select * from users") 
            data = cur.fetchall()

        return render_template('back/email-compose.html' ,data = data) 
    else:
        return redirect('/login')
    
##
# @
# /email-read.html
# 
@app.route('/read/<string:idMessage>', methods = ['POST','GET'])
def red(idMessage):
    if 'okey' in session:
        with sqlite3.connect("nila.db") as con:
            cur = con.cursor()
            cur.execute("select * from messages where idMessage = ?",[idMessage])  
            data = cur.fetchone()

        return render_template('back/email-read.html', data = data)  
    else:
        return redirect("/login")   

@app.route('/composer')
def composer():
    return 'composer' 
if __name__ == '__main__':
    app.run(debug= True)
