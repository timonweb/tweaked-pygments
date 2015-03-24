# Tweaked pygments for Django

Tweaks django-pygments templatetag to not to strip **p** and **br** tags from code snippets.

# Installation
* Put tweaked_pygments under your path
* Add **tweaked_pygments** to INSTALLED_APPS

# Usage
     {% load tweaked_pygmentify %}

* Instead of `{% pygments %}` and `{% endpygments %}`, use `{% tweaked_pygments %}` and `{% endtweaked_pygments %}`   
* Instead of `pygmentify` filter use `tweaked_pygmentify`
* Instead of `pygmentify_inline` filter use `tweaked_pygmentify_inline`
