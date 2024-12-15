from flask import Flask , render_template , redirect , session 
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






if __name__ == '__main__':
    app.run(debug= True)
