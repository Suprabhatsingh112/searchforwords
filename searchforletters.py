from flask import Flask , render_template , request , session , escape, redirect, url_for
import mysql.connector
from vsearch import search4letters
from checker import check_logged_in

app = Flask(__name__)

dbconfig = {'host':'localhost',
            'user':'root',
            'password':'6206086329@bittu',
            'database':'vsearchlogdb'}

def log_request(req:'flask_request', res:str) -> None:

    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        _SQL = """insert into log
               (phrase, letters, ip, results)
               values
               (%s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        res,))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.errors.InterfaceError:
        print('check your database configuration')
    except mysql.connector.errors.ProgrammingError:
        print('please check your code')
    except Exception as err:
        print('something went wrong', str(err))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results'
    results = str(serch4letters(phrase, letters))

    try:
        log_request(request, results)
    except Exception as err:
        print('**logging failed with this error:', str(err))

    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_tittle=title,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_tittle='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        _SQL = """select phrase, letters,ip,results
                          from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)
        conn.close()
        cursor.close()
    except Exception as err:
        print('Something went wrong:', str(err))


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html')
    return render_template('login.html')


@app.route('/login',methods=['POST','GET'])
def do_login() -> str:
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')




@app.route('/logout')
def do_logout() -> str:
    session.pop('username')
    return render_template('logout.html')


app.secret_key = '6206086329123456'

if __name__ == '__main__':
    app.run(debug=True)
