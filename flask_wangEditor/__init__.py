# -*- coding: utf-8 -*-
"""
    flask_wangeditor
    ~~~~~~~~~~~~~~~

    :author: Nuctori <Nuctori@foxmail.com>
    :copyright: (c) 2020 by Nuctori.
    :license: MIT, see LICENSE for more details.
"""
from flask import current_app, Markup, Blueprint, url_for

from flask_wangEditor.fields import WangEditorField  # noqa
from flask_wangEditor.utils import get_url, random_filename  # noqa


class _WangEditor(object):
    """The class implement functions for Jinja2 template."""

    @staticmethod
    def load(custom_url=None, serve_local=None):
        """Load WangEditor resource from CDN or local."""

        if serve_local or current_app.config['WANGEDITOR_SERVE_LOCAL']:
            url = url_for('wangeditor.static', filename='wangEditor.min.js')
        else:
            url = '//unpkg.com/wangeditor/release/wangEditor.min.js'
        if custom_url:
            url = custom_url
        return Markup('<script src="%s"></script>' % url)


    @staticmethod  # noqa
    def config(name='editor', jsObjName=None,custom_config='', **kwargs):


        def format_bool(bool_):
            if bool_ is True:
                return 'true'
            elif bool_ is False:
                return 'false'
            return ValueError('param type must be bool')



        language = str(dict([(str(x),str(y)) for x,y in kwargs.get('language', current_app.config['WANGEDITOR_LANGUAGE']).items()]))
        menus = str(list(map(str,kwargs.get('menus', current_app.config['WANGEDITOR_MENUS']))))
        debug = format_bool(kwargs.get('debug', current_app.config['WANGEDITOR_DEBUG']))
        zIndex = kwargs.get('zIndex', current_app.config['WANGEDITOR_ZINDEX'])
        pasteFilterStyle = format_bool(kwargs.get('pasteFilterStyle', current_app.config['WANGEDITOR_PARSER_FILTER_STYLE']))
        pasteIgnoreImg = format_bool(kwargs.get('pasteIgnoreImg', current_app.config['WANGEDITOR_PARSER_IGNORE_IMG']))

        javascript ='''
<script type="text/javascript">
    let editor = new window.wangEditor('#%s_editor')
    editor.customConfig.menus = %s
    editor.customConfig.debug = %s
    editor.customConfig.zIndex = %s
    editor.customConfig.lang = %s
    editor.customConfig.pasteFilterStyle = %s
    editor.customConfig.pasteIgnoreImg = %s 
    

    editor.customConfig.onchange = function (html) {
        // wangEditor 只支持使用div 为了使用 wtf 这里添加个回调让编辑器的内容和隐藏表单同步
        // 详情 https://www.kancloud.cn/wangfupeng/wangeditor3/430149
        document.getElementById("%s").value=html;
        tempText = editor.txt.html();
    }
    editor.create()
</script>'''
        return Markup(javascript % (name,menus,debug,zIndex,language,pasteFilterStyle,pasteIgnoreImg,name))

    @staticmethod
    def create(name='editor', value=''):
        """Create a wangeditor textarea directly.

        :param name: The name attribute of editor, set it when you need to create
            more than one editor in one page. Default to ``editor``.
        :param value: The preset value for textarea.

        .. versionadded:: 0.3
        """
        return Markup('<div class="wangEditor" id="%s">%s</div>' % (name, value))


class WangEditor(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint('wangeditor', __name__,
                              static_folder='static', static_url_path='/wangeditor' + app.static_url_path)
        app.register_blueprint(blueprint)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['ckeditor'] = _WangEditor()
        app.context_processor(self.context_processor)

        app.config.setdefault('WANGEDITOR_SERVE_LOCAL', False)
        app.config.setdefault('WANGEDITOR_LANGUAGE', {})
        app.config.setdefault('WANGEDITOR_MENUS', [
        'head',
        'bold',
        'italic',
        'underline'
    ])
        app.config.setdefault('WANGEDITOR_DEBUG', False)
        app.config.setdefault('WANGEDITOR_ZINDEX', 10000)
        app.config.setdefault('WANGEDITOR_PARSER_FILTER_STYLE', True)
        app.config.setdefault('WANGEDITOR_PARSER_IGNORE_IMG', False)



    @staticmethod
    def context_processor():
        return {'wangeditor': current_app.extensions['ckeditor']}


