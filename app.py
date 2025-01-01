from flask import Flask , render_template , redirect , session , request , flash
import sqlite3 





app = Flask(__name__)
app.secret_key = 'Nyla_application'

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

        with sqlite3.connect("courses.db") as con :
            cur = con.cursor()
            cur.execute("select * from users where fullNames = ? or phoneUser = ?  and passwordUser = ?", [user,user,pwd])
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
    
    return redirect('/login')


##
#
# creation du compte 
@app.route("/register",methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        pwd  = request.form['pwd']
        pwd2 = request.form['pwd2'] 

        # verification du double mot de passe 
        if pwd == pwd2:
            with sqlite3.connect("courses.db") as con :
                cur = con.cursor()
                cur.execute("insert into users(fullNames,passwordUser) values(?,?)",[user,pwd])
                con.commit()
                return redirect('/login')
        else:
            flash("les mot de passe doivent etre identique")
    return render_template('back/page-register.html')

if __name__ == '__main__':
    app.run(debug= True)
