from urllib.parse import urlencode

from django import forms

from hcaptcha.settings import JS_API_URL, SITEKEY

import json

import django
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import get_language


class hCaptchaWidget(forms.Widget):
    template_name = 'hcaptcha_widget.html'

    def __init__(self, *args, **kwargs):
        self.extra_url = {}
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return data.get('h-captcha-response')

    def render(self, name, value, attrs=None, renderer=None):
        if django.VERSION < (1, 11):
            return mark_safe(render_to_string(
                self.template_name,
                self.get_context(name, value, attrs)
            ))
        else:
            return super(hCaptchaWidget, self).render(
                name, value, attrs=attrs, renderer=renderer
            )

    def get_context(self, name, value, attrs):

        try:
            lang = attrs['lang']
        except KeyError:
            # Get the generic language code
            lang = get_language().split('-')[0]

        context = {
            "widget": {
                "attrs": self.build_attrs(attrs)
            }
        }
        context['widget']['attrs']['data-sitekey'] = SITEKEY
        context.update({
            'api_url': JS_API_URL,
            'data-sitekey': SITEKEY,
            'lang': lang,
            'options': mark_safe(json.dumps(self.attrs, indent=2)),
        })

        return context
