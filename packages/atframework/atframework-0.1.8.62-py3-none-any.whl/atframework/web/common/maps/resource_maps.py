"""
Created on Mar 04, 2021

@author: Siro

"""

import os
import platform
import sys
from atframework.web.utils.utils import Utils


class ResourceMaps(object):
    utils = Utils()
    setupPropertiesPath = utils.get_setup_properties_path()
    setupInfo = utils.get_setup_info(setupPropertiesPath)
    documentImagePath = utils.get_document_image_path()

    '''
    site setup info
    '''
    RUNNING_SITE = setupInfo['site']

    if utils.site == "":
        running_site = RUNNING_SITE
    else:
        running_site = str(utils.site)

    '''
    set the current browser
    '''
    if utils.browser == "":
        BROWSER_NAME = setupInfo['browser']
    else:
        BROWSER_NAME = str(utils.browser)

    propertiesPath = os.path.abspath(os.path.dirname(os.getcwd(
    ))) + "/properties/" + running_site + "/integration.properties"
    dicProperties = utils.get_all_properties(propertiesPath)

    '''
    site protection info
    '''
    PROTECTION_USERNAME = dicProperties['protectionUsername']
    PROTECTION_PASSWORD = dicProperties['protectionPassword']

    '''
    the following are web site links
    '''
    SITE_ADDRESS = dicProperties['siteProtal']
    SITE_ADDRESS_EN = dicProperties['siteProtalEN']

    '''
    the following are BO links
    '''
    BO_ADDRESS = dicProperties['boProtal']

    '''
    the following are BO Admin account info
    '''
    USERNAME_BO = dicProperties['usernameBo']
    PASSWORD_BO = dicProperties['passwordBo']

    '''
    the following test account info should be changed before testing
    '''
    TEST_EMAIL = utils.get_test_user_name() + "@test.com"
    TEST_EMAIL_PREFIX = utils.get_test_user_name_prefix()
    TEST_NICKNAME = utils.get_test_user_name()
    TEST_PASSWORD = dicProperties['testPasswrod']

    '''
    profile page
    '''
    STREET_NUMBER = dicProperties['streetNumber']
    HOUSE_NUMBER = dicProperties['houseNumber']
    DISTRICT = dicProperties['district']
    CITY = dicProperties['city']
    ZIP_CODE = dicProperties['zipCode']
    PHONE_NUMBER = utils.get_phone_number()
    BIRTH_DAY = dicProperties['birthday']
    BIRTH_MONTH = dicProperties['birthmonth']
    BIRTH_MONTH_ENGLISH = dicProperties['birthmonthEnglish']
    BIRTH_YEAR = dicProperties['birthyear']
    DOCUMENT_NAME = dicProperties['documentName']
    DOCUMENT_IMAGE_PATH = documentImagePath

    '''
    testing account
    '''
    USERID = dicProperties['userid']
    USER_EMAIL = dicProperties['userEmail']
