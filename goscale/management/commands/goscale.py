# -*- coding: utf-8 -*-
from __future__ import absolute_import
from cms.management.commands.subcommands.base import SubcommandsCommand
from goscale.management.commands.subcommands.debug import Debug
from goscale.management.commands.subcommands.dump import Dump
from goscale.management.commands.subcommands.load import Load
from goscale.management.commands.subcommands.update_posts import UpdatePosts
from goscale.management.commands.subcommands.update_slugs import UpdateSlugs
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(SubcommandsCommand):
    args = '<subcommand>'

    option_list = BaseCommand.option_list + (
        make_option('-s', '--site', default=None,
                    help='Site ID to filter plugins.'),
        make_option('-t', '--theme', default=None,
                    help='Theme name to filter plugins.'),
    )

    command_name = 'goscale'

    subcommands = {
        'debug': Debug,
        'dump': Dump,
        'load': Load,
        'update_posts': UpdatePosts,
        'update_slugs': UpdateSlugs,
    }

    @property
    def help(self):
        lines = ['GoScale CMS command line interface.', '', 'Available subcommands:']
        for subcommand in sorted(self.subcommands.keys()):
            lines.append('  %s' % subcommand)
        lines.append('')
        lines.append('Use `manage.py %s <subcommand> --help` for help about subcommands' % self.command_name)
        return '\n'.join(lines)
