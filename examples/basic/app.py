# -*- coding: utf-8 -*-
"""
    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_wangEditor import WangEditor, WangEditorField

app = Flask(__name__)
app.config['WANGEDITOR_SERVE_LOCAL'] = True
app.secret_key = 'secret string'

ckeditor = WangEditor(app)


class PostForm(FlaskForm):
    title = StringField('Title')
    body = WangEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        # You may need to store the data in database here
        return render_template('post.html', title=title, body=body)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
