#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json
import os

CONFIG_CACHE = None


class Configuration:
    # USER_API_URI = 'http://localhost:8000'
    # DATA_API_URI = 'http://localhost:8001'
    # ANNOTATION_API_URI = 'http://localhost:8002'
    USER_API_URI = 'https://userapi-dev-7mvc6un3ya-ez.a.run.app'
    DATA_API_URI = 'https://dataapi-dev-7mvc6un3ya-ez.a.run.app'
    ANNOTATION_API_URI = 'https://annotationapi-dev-7mvc6un3ya-ez.a.run.app'

    def __getitem__(self, config_parameter):
        config = self.get_config()
        return config[config_parameter]

    def __contains__(self, config_parameter):
        config = self.get_config()
        return config_parameter in config

    def __setitem__(self, config_parameter, value):
        config = self.get_config()
        config[config_parameter] = value

    def __delitem__(self, config_parameter):
        config = self.get_config()
        del config[config_parameter]

    def get_home_dir(self):
        user_home_dir = os.getenv("HOME")
        return os.path.join(user_home_dir, '.xplai')

    def get_cached_api_key(self) -> (str, str):
        if 'api_key' not in self or 'username' not in self:
            raise UserIsNotAuthorizedException

        return self['api_key'], self['username']

    def get_api_headers(self):
        api_key, username = self.get_cached_api_key()
        return {'api_key': api_key, 'username': username}

    def get_config(self,
                   reload=False
                   ):
        global CONFIG_CACHE

        if reload is True or CONFIG_CACHE is None:
            file_name = self.__get_config_file_name()
            if os.path.exists(file_name):
                CONFIG_CACHE = self.__load_from_file(file_name)
                return CONFIG_CACHE
            else:
                CONFIG_CACHE = {}
                self.__save_to_file(file_name)

        return CONFIG_CACHE

    def save(self):
        file_name = self.__get_config_file_name()
        self.__save_to_file(file_name)

    def __load_from_file(self,
                         file_name):
        global CONFIG_CACHE
        with open(file_name, 'r') as j:
            CONFIG_CACHE = json.load(j)
        return CONFIG_CACHE

    def __save_to_file(self,
                       file_name):
        global CONFIG_CACHE
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w') as file:
            json.dump(CONFIG_CACHE, file, sort_keys=True, indent=4)

    def __get_config_file_name(self):
        user_home_dir = os.getenv("HOME")
        return os.path.join(user_home_dir, '.xplai', 'config.json')


class UserIsNotAuthorizedException(Exception):
    pass
