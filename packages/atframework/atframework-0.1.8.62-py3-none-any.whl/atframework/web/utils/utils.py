'''
Created on Mar 03, 2021

@author: Siro

'''

import random
import datetime
import re
import os

from atframework.web.utils.properties import Properties


class Utils(object):
    site = ""
    browser = ""

    '''
    Get Random phone number from 100000-99999999999
    '''

    def get_phone_number(self):
        number = random.randint(100000, 99999999999)
        phoneNumber = str(number)
        return phoneNumber

    '''
    Get Random number from 1-10000
    '''

    def get_test_user_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 100000)
        # abc98656
        username = str(name1) + str(name2) + str(name3) + str(number)
        return username

    def get_test_user_name_prefix(self, randint=random.randint(0, 10)):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = randint
        # abc9
        usernamePrefix = str(name1) + str(name2) + str(name3) + str(number)
        return usernamePrefix

    def get_all_properties(self, properties_path):
        dictProperties = Properties(properties_path).getProperties()
        return dictProperties

    def get_setup_info(self, properties_path):
        dictInfos = Properties(properties_path).getProperties()
        return dictInfos

    def override_setup_properties(self, file_path, opt_key, opt_value):
        try:
            file_data = ""
            with open(file_path, 'r', encoding='utf-8') as read_setup_properties:
                file_str = read_setup_properties.readlines()
                for line in file_str:
                    line = line.strip().replace('\n', '')
                    find_str = opt_key + '='
                    opt_key_index = line.find(find_str)
                    line_content = line
                    if opt_key_index is not -1:
                        re_file_str = line[(opt_key_index + len(find_str)):]
                        line_content = line.replace(re_file_str, opt_value)
                    file_data += line_content + "\n"
            with open(file_path, 'w', encoding='utf-8') as write_setup_properties:
                write_setup_properties.writelines(file_data)
        except Exception as e:
            raise e

    def get_integration_properties_path(self, site):
        return os.path.abspath(os.path.dirname(os.getcwd(
        ))) + "/properties/" + str(site) + "/integration.properties"

    def get_setup_properties_path(self):
        return os.path.abspath(os.path.dirname(
            os.getcwd())) + "/properties/setup.properties"

    def get_document_image_path(self):
        return os.path.abspath(os.path.dirname(
            os.getcwd())) + '/atframework/web/common/images/testDocument.jpg'