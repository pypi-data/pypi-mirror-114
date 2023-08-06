#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import argparse
import sys

from getpass import getpass

from xplai.configuration import UserIsNotAuthorizedException
from xplai.cli import annotations, auth, concept, modality, task


OFFSET = '  '


def main():
    try:
        parser = argparse.ArgumentParser(description='XPL SDK')
        parser.add_argument("module")
        parser.add_argument("command")

        args = parser.parse_args(sys.argv[1:3])
        if args.module.lower() == 'task':
            if args.command.lower() == 'create' or args.command.lower() == 'draft':
                parser = argparse.ArgumentParser()
                parser.add_argument('-m', '--modality')
                parser.add_argument('-n', '--name')
                parser.add_argument('-c', '--csv')
                sub_args = parser.parse_args(sys.argv[3:])

                modality_id = input("Provide task modality :") if sub_args.modality is None else sub_args.modality
                name = input("Provide task name :") if sub_args.name is None else sub_args.name
                csv = input("Specify path to csv file with examples :") if sub_args.csv is None else sub_args.csv

                result = task.create_from_csv(name=name,
                                              modality=modality_id,
                                              path_to_csv=csv)
                print(result)
            elif args.command.lower() == 'commit':
                print(task.commit_draft())
            elif args.command.lower() == 'list':
                print(task.list_tasks())
            elif args.command.lower() == 'describe':
                parser = argparse.ArgumentParser()
                parser.add_argument('-t', '--task_id')
                sub_args = parser.parse_args(sys.argv[3:])
                print(task.describe(sub_args.task_id))
            else:
                raise Exception(f'unknown command {args.command}')

        elif args.module.lower() == 'annotations':
            if args.command.lower() == 'list':
                parser = argparse.ArgumentParser()

                parser.add_argument('-t', '--task_id')
                sub_args = parser.parse_args(sys.argv[3:])
                task_id = input("Provide task_id :") if sub_args.task_id is None else sub_args.task_id

                print(annotations.list_annotation_jobs(task_id=task_id))
            else:
                raise Exception(f'unknown command {args.command}')

        elif args.module.lower() == 'concept':
            if args.command.lower() == 'search':
                if len(sys.argv[3:]) < 2:
                    while True:
                        lemma = input("lemma :")
                        search_result_text, _ = concept.search(lemma=lemma, include_not_found_option=False)
                        print(search_result_text)
                else:
                    parser = argparse.ArgumentParser()
                    parser.add_argument('-l', '--lemma')
                    sub_args = parser.parse_args(sys.argv[3:])
                    lemma = sub_args.lemma
                    search_result_text, _ = concept.search(lemma=lemma, include_not_found_option=False)
                    print(search_result_text)

        elif args.module.lower() == 'modality':
            if args.command.lower() == 'list':
                print(modality.list_supported_modalities())

        elif args.module.lower() == 'auth':
            if args.command.lower() == 'login':
                if len(sys.argv[3:]) < 2:
                    username = input("username :")
                    secret = getpass("secret :")
                else:
                    parser = argparse.ArgumentParser()
                    parser.add_argument('-u', '--username')
                    parser.add_argument('-s', '--secret')

                    sub_args = parser.parse_args(sys.argv[3:])
                    username = sub_args.username
                    secret = sub_args.secret

                login_result_message = auth.login(username, secret)
                print(login_result_message)
            elif args.command.lower() == 'logout':
                logout_result = auth.logout()
                print(logout_result)
            else:
                raise Exception(f'unknown command {args.command}')

        else:
            raise Exception(f'unknown command {args.module}')
    except UserIsNotAuthorizedException:
        print(f'{OFFSET}User is not authenticated. To login type:\n')
        print(f'{OFFSET}xpl auth login\n')


if __name__ == '__main__':
    main()
