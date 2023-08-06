"""
Created on Mar 28, 2021

@author: Siro

"""

from atframework.web.common.model.model import Model


class BoRebate(Model):
    """
    Inherit the basic GUI action, and expand some methods on BO Rebate
    """

    def open_rebate_menu(self, xpath):
        self._click_link_by_xpath(xpath)

    def open_rebate_instance_search(self, css_selector):
        self._click_link_by_css(css_selector)

    def is_opened_rebate_instance_search(self, css_selector):
        return self._find_link_by_css(css_selector)

    def open_create_new_rebate_instance(self, css_selector):
        self._click_link_by_css(css_selector)

    def is_opened_create_new_rebate_instance(self, css_selector):
        return self._find_link_by_css(css_selector)
