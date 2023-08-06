"""
Created on July 26, 2021

@author: Siro

"""


class BoLoginElementsMaps(object):
    """
    store the web elements in this Class
    """
    protection_page_logo_xpath = "//*[@id='logo']/img"
    protection_username_css = "input[type='text'][id='username'][name='siteProtectionUsername']"
    protection_password_css = "input[id='password'][name='siteProtectionPassword'][type='password']"
    protection_login_css = "input[class='btn btn-primary'][value='Login'][title='Login'][type='submit']"

    bo_username_field_css = "input[id='login_username'][class='bo-field__control form-control bo-field__control--textfield validation-required']"
    bo_username_filed_xpath = "//*[@id='login_username']"
    bo_password_field_css = "input[id='login_password'][class='bo-field__control form-control bo-field__control--password validation-required']"
    bo_login_button_css = "button[id='login_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
