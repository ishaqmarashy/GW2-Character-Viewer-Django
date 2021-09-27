from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from tabulate import tabulate
app= Flask(__name__)

# MySQL configurations
username ='root'
password=''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = username
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'fooddb'
mysql = MySQL(app)
app.config['SQLALCHEMY_URI']=f"mysql://{username}:{password}@locathost"
app.config['SECRET_KEY']='777'
item=''
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('''Show Tables''')
    df = cursor
    cursor.close()
    item=(tabulate(df, tablefmt = 'html'))
    return render_template('index.html',message=item)

@app.route('/submit',methods=['POST'])
def submit():
    if request.method=='POST':
        b=request.form['login']
        a=request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT {a} from {b}''')
        df = cursor
        cursor.close()
        if a and b:
            item2=(tabulate(df,  tablefmt = 'html'))
            return render_template('index.html',message=item,message2=item2)
        return render_template('index.html')

if __name__=='__main__':
    app.debug=false
    app.run()

