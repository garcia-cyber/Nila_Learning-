from flask import Flask , render_template , redirect , session 




app = Flask(__name__)
app.secret_key = 'Nyla_application'


@app.route('/')
@app.route('/home')
def home():
    return render_template('front/index.html')






if __name__ == '__main__':
    app.run(debug= True)
