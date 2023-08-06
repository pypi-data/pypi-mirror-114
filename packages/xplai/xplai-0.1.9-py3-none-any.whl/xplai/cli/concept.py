#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

from typing import List

from xplai.api import concept_api_client
from xplai.api.concept_api_client import Concept
from xplai.cli import utils

OFFSET = '  '


def search(lemma: str,
           include_not_found_option: bool = False,
           ) -> (str, List[Concept]):
    search_results = concept_api_client.search(lemma=lemma)
    search_results_text = ''
    if len(search_results) > 0:
        search_results_text += utils.print_table(search_results, ['pos', 'name', 'definition'])

        if include_not_found_option is True:
            search_results_text += f'\n[{len(search_results)}] ' \
                                   f'{OFFSET}Nothing from above. Create new concept={lemma}. \n'
            search_results.append(Concept(name=lemma))
    else:
        search_results_text += f'\n{OFFSET}Nothing was found for "{lemma}"\n'
        if include_not_found_option is True:
            search_results_text += f'\n[{len(search_results)}] Create new concept={lemma}. \n'
            search_results.append(Concept(name=lemma))

    return search_results_text, search_results


class BColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def __color_code_pos(pos: str
                     ) -> str:
    color = ''
    if pos == 'NOUN':
        color = BColors.BLUE
    elif pos == 'VERB':
        color = BColors.RED
    elif pos == 'ADJECTIVE' or pos == 'ADJECTIVE SATELLITE':
        color = BColors.ORANGE
    elif pos == 'ADVERB':
        color = BColors.GREEN
    return f'{color}{pos}{BColors.ENDC}'

# def ask_user_to_choose(concepts: List[Concept], message: str, lemma: str):
#     choices = [f'0:  {"Not in the list.":24s}  Create new from the name={lemma}?']
#     for idx, c in enumerate(concepts):
#         if c.concept_id is not None:
#             choice = f'{str(idx + 1) + ":":3s} {"(" + c.concept_id + ")":24s} ({c.pos})  {c.definition}'
#         elif c.wn_id is not None:
#             choice = f'{str(idx + 1) + ":":3s} {"(" + c.wn_id + ")":24s} ({c.pos}) {c.definition}'
#         else:
#             choice = f'{str(idx + 1) + ":":3s} {"(" "":24s + ")"} ({c.pos}) {c.name} {c.definition}'
#
#         choices.append(choice)
#
#     default_choice = 1 if len(concepts) > 0 else 0
#     questions = [inquirer.List(name='_', message=message, choices=choices, default=choices[default_choice])]
#
#     answers = inquirer.prompt(questions)
#
#     answer = answers['_']
#     idx = int(answer.split(':')[0].strip())
#
#     if idx == 0:
#         raise NoAppropriateConceptException()
#
#     return concepts[idx - 1]
#
#
# class NoAppropriateConceptException(Exception):
#     pass
