import os
from uuid import uuid4
import flask
from random import randint
from PIL import Image


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
        elif flask.request.form.get('action') == 'in_img':
            file = flask.request.files['in_img']
            if file:  # and allowed_file(file.filename):
                im = Image.open(file)
                im = im.convert('RGBA')
                im = im.resize((randint(150, 200), randint(150, 200)))
                pix = im.load()
                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                        pix[x, y] = (0, pix[x, y][2], 0, 255)

                filename = uuid4().hex
                im.save(os.path.join('media', 'uploads', filename), 'JPEG')

                entry = Entry(filename, Entry.TYPE_IMG)
                db.session.add(entry)
                db.session.commit()
            else:
                errors.append('img')
    return flask.render_template('index.html',
                                 text_entries=Entry.get_text_entries(),
                                 img_entries=Entry.get_img_entries(),
                                 random=randint,
                                 fonts=fonts,
                                 errors=errors)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8888)
