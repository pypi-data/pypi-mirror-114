import argparse
import os
from typing import List


def api_to_dict():
    """Convert Jina API to a dict
    :return: dict
    """
    from jina import __version__
    from jina.parsers import get_main_parser

    all_d = {
        'name': 'Jina',
        'description': 'Jina is the cloud-native neural search solution powered by state-of-the-art AI and deep '
        'learning technology',
        'license': 'Apache 2.0',
        'vendor': 'Jina AI Limited',
        'source': 'https://github.com/jina-ai/jina/tree/'
        + os.environ.get('JINA_VCS_VERSION', 'master'),
        'url': 'https://jina.ai',
        'docs': 'https://docs.jina.ai',
        'authors': 'dev-team@jina.ai',
        'version': __version__,
        'methods': [],
        'revision': os.environ.get('JINA_VCS_VERSION'),
    }

    def get_p(p, parent_d):
        parsers = p()._actions[-1].choices
        for p_name in parsers.keys():
            d = {'name': p_name, 'options': [], 'help': parsers[p_name].description}
            for ddd in _export_parser_args(
                lambda *x: p()._actions[-1].choices[p_name], type_as_str=True
            ):
                d['options'].append(ddd)

            if not d['options']:
                d['methods'] = []
                get_p(lambda *x: parsers[p_name], d)
            parent_d['methods'].append(d)

    get_p(get_main_parser, all_d)

    return all_d


def _export_parser_args(parser_fn, type_as_str: bool = False, **kwargs):
    from jina.enums import BetterEnum
    from argparse import _StoreAction, _StoreTrueAction
    from jina.parsers.helper import KVAppendAction, _SHOW_ALL_ARGS

    port_attr = ('help', 'choices', 'default', 'required', 'option_strings', 'dest')
    parser = parser_fn(**kwargs)
    parser2 = parser_fn(**kwargs)
    random_dest = set()
    for a, b in zip(parser._actions, parser2._actions):
        if a.default != b.default:
            random_dest.add(a.dest)
    for a in parser._actions:
        if isinstance(a, (_StoreAction, _StoreTrueAction, KVAppendAction)):
            if not _SHOW_ALL_ARGS and a.help == argparse.SUPPRESS:
                continue
            ddd = {p: getattr(a, p) for p in port_attr}
            if isinstance(a, _StoreTrueAction):
                ddd['type'] = bool
            elif isinstance(a, KVAppendAction):
                ddd['type'] = dict
            else:
                ddd['type'] = a.type
            if ddd['choices']:
                ddd['choices'] = [
                    str(k) if isinstance(k, BetterEnum) else k for k in ddd['choices']
                ]
                ddd['type'] = str
            if isinstance(ddd['default'], BetterEnum):
                ddd['default'] = str(ddd['default'])
                ddd['type'] = str
            if ddd['type'] == str and (a.nargs == '*' or a.nargs == '+'):
                ddd['type'] = List[str]
        else:
            continue

        if a.dest in random_dest:
            ddd['default_random'] = True
            from jina.helper import random_identity, random_port

            if isinstance(a.default, str):
                ddd['default_factory'] = random_identity.__name__
            elif isinstance(a.default, int):
                ddd['default_factory'] = random_port.__name__
        else:
            ddd['default_random'] = False

        if type_as_str:
            ddd['type'] = getattr(ddd['type'], '__name__', str(ddd['type']))
        ddd['name'] = ddd.pop('dest')
        yield ddd
