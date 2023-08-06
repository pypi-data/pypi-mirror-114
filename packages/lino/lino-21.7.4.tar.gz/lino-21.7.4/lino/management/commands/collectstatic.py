# -*- coding: UTF-8 -*-
# Copyright 2009-2021 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStatic
from django.conf import settings

from lino.modlib.help.management.commands.makehelp import Command as MakeHelp


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.collect_static = CollectStatic(*args, **kwargs)
        self.make_help = MakeHelp(*args, **kwargs)

    def add_arguments(self, parser):
        self.collect_static.add_arguments(parser)
        self.make_help.add_arguments(parser)

        parser.add_argument(
            '--skip-cachebuild', '--skip-cache-build', action='store_true',
            dest='skip_cache', help="Do NOT build site cache.")
        parser.add_argument(
            '--skipcollect', '--skip-collect', action='store_true',
            dest='skip_collect', help="Build site cache only.")
        parser.add_argument(
            '--skiphelp', '--skip-help', action='store_true',
            dest='skip_help', help="Build site cache only.")

    def handle(self, **options):
        if not options['skip_cache']:
            settings.SITE.kernel.default_ui.renderer.build_site_cache(
                force=True, from_commandline=True)

        if not options['skip_help']:
            self.make_help.handle(**options)

        if not options['skip_collect']:
            self.collect_static.handle(**options)
