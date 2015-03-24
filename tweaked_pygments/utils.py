from django_pygments.utils import ListHtmlFormatter
import warnings

warnings.simplefilter('ignore')
from pygments.lexers import LEXERS, get_lexer_by_name

warnings.resetwarnings()
from pygments import highlight
import re
from django.utils.encoding import smart_text
from functools import reduce


def tweaked_pygmentify_html(text, **kwargs):
    text = smart_text(text)
    lang = default_lang = 'text'
    # a tuple of known lexer names
    try:
        lexers_iter = LEXERS.itervalues()
    except AttributeError:
        lexers_iter = LEXERS.values()
    lexer_names = reduce(lambda a, b: a + b[2], lexers_iter, ())
    # custom formatter
    formatter = ListHtmlFormatter(encoding='utf-8', **kwargs)
    subs = []
    pre_re = re.compile(r'(<pre[^>]*>)(.*?)(</pre>)', re.DOTALL | re.UNICODE)
    # Comment out br_re to stop pygments from stripping <br/> tag in code snippets.
    # br_re = re.compile(r'<br[^>]*?>', re.UNICODE)
    # Comment out p_re to stop pygments from stripping <p> and </p> in code.
    # p_re = re.compile(r'<\/?p[^>]*>', re.UNICODE)
    lang_re = re.compile(r'lang=["\'](.+?)["\']', re.DOTALL | re.UNICODE)
    for pre_match in pre_re.findall(text):
        work_area = pre_match[1]
        #work_area = br_re.sub('\n', work_area)
        match = lang_re.search(pre_match[0])
        if match:
            lang = match.group(1).strip()
            if lang not in lexer_names:
                lang = default_lang
        lexer = get_lexer_by_name(lang, stripall=True)
        work_area = work_area.replace(u'&nbsp;', u' ').replace(u'&amp;', u'&').replace(u'&lt;', u'<').replace(u'&gt;',
                                                                                                              u'>').replace(
            u'&quot;', u'"').replace(u'&#39;', u"'")
        #work_area = p_re.sub('', work_area)
        work_area = highlight(work_area, lexer, formatter)
        subs.append([u''.join(pre_match), smart_text(work_area)])
    for sub in subs:
        text = text.replace(sub[0], sub[1], 1)
    return text