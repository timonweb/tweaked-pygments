from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from django_pygments.templatetags.pygmentify import PygmentifyNode
from ..utils import tweaked_pygmentify_html


register = template.Library()


@register.filter
@stringfilter
def tweaked_pygmentify(value):
    try:
        res = tweaked_pygmentify_html(value)
    except Exception as e:
        print(e)
        print(u'value="%s"' % value)
        res = value
    return mark_safe(res)


@register.filter
@stringfilter
def tweaked_pygmentify_inline(value):
    try:
        res = tweaked_pygmentify_html(value, noclasses=True)
    except Exception as e:
        print(e)
        print(u'value="%s"' % value)
        res = value
    return mark_safe(res)


class TweakedPygmentifyNode(PygmentifyNode):
    def render(self, context):
        output = self.nodelist.render(context)
        try:
            res = tweaked_pygmentify_html(output, **self.kwargs)
        except Exception as e:
            print(e)
            print(u'value="%s"' % output)
            res = output
        return mark_safe(res)


@register.tag
def tweaked_pygment(parser, token):
    token_args = token.split_contents()
    kwargs = {}
    for item in token_args[1:]:
        kw_parts = [i.strip() for i in item.split('=')]
        # we intentionally leave kw_parts[1] as is without any
        # exception handling so that if the argument supplied is
        # not of the keyword argume type, the error is propogated
        kwargs[kw_parts[0]] = eval(kw_parts[1])

    nodelist = parser.parse(('endtweaked_pygment',))
    parser.delete_first_token()
    return TweakedPygmentifyNode(nodelist, **kwargs)
