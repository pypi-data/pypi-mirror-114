# -*- coding: UTF-8 -*-
# Copyright 2009-2021 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.staticfiles.management.commands.collectstatic import Command
from django.conf import settings


class Command(Command):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--no-cachebuild', '--no-cache-build', action='store_true',
            dest='no_cache', help="Do NOT build site cache.")
        parser.add_argument(
            '--cacheonly', '--cache-only', action='store_true',
            dest='cache_only', help="Build site cache only.")

    def handle(self, **options):
        if not options['no_cache']:
            settings.SITE.kernel.default_ui.renderer.build_site_cache(
                force=True, from_commandline=True)

        if not options['cache_only']:
            super().handle(**options)
