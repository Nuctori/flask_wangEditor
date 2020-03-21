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
        autoSave = format_bool(kwargs.get('autoSave', current_app.config['WANGEDITOR_AUTO_SAVE']))

        editorInitScript = '''
    let editor = new window.wangEditor('#{name}_editor')
    editor.customConfig.menus = {menus}
    editor.customConfig.debug = {debug}
    editor.customConfig.zIndex = {zIndex}
    editor.customConfig.lang = {language}
    editor.customConfig.pasteFilterStyle = {pasteFilterStyle}
    editor.customConfig.pasteIgnoreImg = {pasteIgnoreImg}
'''.format(name=name,menus=menus,zIndex=zIndex,language=language,pasteFilterStyle=pasteFilterStyle,pasteIgnoreImg=pasteIgnoreImg,debug=debug)

        editorOnchangeScript = '''
    editor.customConfig.onchange = function (html) {{
        // wangEditor 只支持使用div 为了使用 wtf 这里添加个回调让编辑器的内容和隐藏表单同步
        // 详情 https://www.kancloud.cn/wangfupeng/wangeditor3/430149
        document.getElementById("{name}").value=html;
        tempText = editor.txt.html();
        if ({autoSave}==true && tempText != '') {{ // 自动保存 autoSave
            localStorage.setItem(url, tempText);
        }}
    }}
'''.format(name=name,autoSave=autoSave)

        documentReadyScript = '''
    content = document.getElementById("{name}").value; 

    // 同步input表单和富文本编辑器之间的内容
    if (content != "") {{ 
        editor.txt.html(content);
    }} else {{
        document.getElementById("{name}").value = editor.txt.html()
    }}
    if ({autoSave}==true) {{
        // 载入自动保存的内容
        let comment_history_text = localStorage.getItem(url)
        if (comment_history_text) {{ 
            editor.txt.html(comment_history_text)
        }}
    }}
'''.format(autoSave=autoSave,name=name)

        javascript ='''
<script type="text/javascript">
    let url = window.location.href;
    {editorInitScript}
    {editorOnchangeScript}
    editor.create()
    {documentReadyScript}
</script>'''
        return Markup(javascript.format(editorInitScript=editorInitScript,editorOnchangeScript=editorOnchangeScript,documentReadyScript=documentReadyScript))

    @staticmethod
    def create(name='editor', value=''):
        """Create a wangeditor textarea directly.

        :param name: The name attribute of editor, set it when you need to create
            more than one editor in one page. Default to ``editor``.
        :param value: The preset value for textarea.

        .. versionadded:: 0.3
        """
        return Markup('<div class="wangEditor" id="%s">%s</div>' % (name, value))
    

    @staticmethod
    def clean_auto_save():
        '''
        清除编辑器自动保存在本地的数据，一般在表单的onclick事件中使用
        '''
        return 'localStorage.removeItem(window.location.href)'
        


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
        app.extensions['wangEditor'] = _WangEditor()
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
        app.config.setdefault('WANGEDITOR_AUTO_SAVE', False)
        



    @staticmethod
    def context_processor():
        return {'wangeditor': current_app.extensions['wangEditor']}


