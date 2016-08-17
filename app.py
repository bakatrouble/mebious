import flask
from random import randint


app = flask.Flask(__name__, static_folder='media')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

from models import db, Entry

db.init_app(app)

fonts = [
    'Arial,Helvetica,sans-serif',
    'Courier New,Courier,monospace',
    'Georgia,Times New Roman,Times,serif',
    'Times New Roman,Times,serif',
]


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    if flask.request.method == 'POST':
        if flask.request.form.get('action') == 'in_txt':
            if flask.request.form.get('in_txt'):
                entry = Entry(flask.request.form.get('in_txt'), Entry.TYPE_TEXT)
                db.session.add(entry)
                db.session.commit()
            else:
                errors.append('txt')
    return flask.render_template('index.html',
                                 text_entries=Entry.get_text_entries(),
                                 random=randint,
                                 fonts=fonts,
                                 errors=errors)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8888)
