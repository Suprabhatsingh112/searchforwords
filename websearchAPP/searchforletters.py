from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from vsearch import serch4letters
app = Flask(__name__)

def log_request(req:'flask_request', res:str) -> None:
    dbconfig = {'host':'localhost',
                'user':'root',
                'password':'6206086329@bittu',
                'database':'vsearchlogdb'}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log
           (phrase, letters, ip, browser_string, results)
           values
           (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results'
    results = str(serch4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase = phrase,
                           the_letters = letters,
                           the_tittle = title,
                           the_results = results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_tittle='Welcome to search4letters on the web!')
if __name__=='__main__':
    app.run(debug=True)