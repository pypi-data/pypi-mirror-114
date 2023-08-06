"""
Created on July 26, 2021

@author: Siro

"""


class BoHelpdeskElementsMaps(object):

    bo_helpdesk_link_css = "a[class='bo-nav__control'][href='playerSearch!view']"
    bo_search_text_field_css = "input[id='playerSearch_freeText'][class='bo-field__control form-control bo-field__control--textfield']"
    bo_search_text_field_xpath = "//*[@id='playerSearch_freeText']"
    bo_search_button_css = "button[id='playerSearch_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
    bo_user_xpath = ".//*[@id='players']/tbody/tr/td[3]/a"
    bo_account_status_selector_css = "select[id='player_user_userStatus'][class='bo-field__control form-control bo-field__control--select']"
    bo_account_status_selector_active_value = "active"
    bo_update_button_css = "button[id='player_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary'][type='submit']"
    bo_update_1st_button_xpath = ".//*[@id='player_0'][1]"