# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.utils.translation import get_language
from lino.core.actors import Actor
from lino.core.actions import Action
from lino.api import _

class OpenHelpWindow(Action):

    action_name = 'open_help'
    # icon_name = 'help'
    button_text = '?'
    select_rows = False
    help_text = _('Open Help Window')

    def run_from_ui(self, ar, **kwargs):
        # print("20210612")
        parts = ['cache', 'help']
        if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
            parts.append(get_language())
        parts.append(str(ar.actor) + ".html")
        # parts.append("index.html")
        ar.success(open_url=settings.SITE.build_site_cache_url(*parts))

    # def get_a_href_target(self):
    #     parts = ['cache', 'help']
    #     if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
    #         parts.append(get_language())
    #     parts.append("index.html")
    #     return settings.SITE.build_media_url(*parts)


Actor.open_help = OpenHelpWindow()
