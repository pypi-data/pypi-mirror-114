"""
Created on July 26, 2021

@author: Siro

"""


class BoRebateElementsMaps(object):

    bo_rebate_link_xpath = '//*[@id="bo-page-rebate-rebate-instances"]/div/div/div/div/div[1]/nav/div/ul/li[5]/a/span/span'
    bo_rebate_instance_link_css = 'a[class="bo-nav__control"][href="rebateInstances!search?status=ACTIVE"]'
    bo_rebate_create_new_instance_link_css = 'a[class="bo-link bo-filter__link"][href="rebateCreateInstance!view"]'
    bo_rebate_create_new_instance_name_field_css = '//*[@id="rebateCreateInstance_entity_name"]'