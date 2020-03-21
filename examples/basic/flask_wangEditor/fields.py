# -*- coding: utf-8 -*-
"""
    flask_wangeditor
    ~~~~~~~~~~~~~~~

    :author: Nuctori <Nuctori@foxmail.com>
    :copyright: (c) 2020 by Nuctori.
    :license: MIT, see LICENSE for more details.
"""
from wtforms import TextAreaField

from wtforms.widgets.core import HTMLString,html_params,escape
from wtforms.compat import text_type


class WangEditor():
    def __call__(self, field, **kwargs):# create the widget of the wtforms
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % ('wangEditor', c)
        kwargs.setdefault('id', field.id)
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        editor_id = field.name + '_editor'
        return HTMLString('<div id={id} ></div><input hidden=true %s>%s</input>'.format(id=editor_id) % ( 
            html_params(name=field.name, **kwargs),
            escape(text_type(field._value()), quote=False)
        )) # div is the editor, input will get the content from div by onchange callback in js code


class WangEditorField(TextAreaField):
    widget = WangEditor()
