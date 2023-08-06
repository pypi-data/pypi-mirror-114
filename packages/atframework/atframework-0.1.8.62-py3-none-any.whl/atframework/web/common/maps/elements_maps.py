"""
Created on Mar 04, 2021

@author: Siro

"""
from atframework.web.common.maps.bo.bo_header_elements_maps import BoHeaderElementsMaps
from atframework.web.common.maps.bo.bo_login_elements_maps import BoLoginElementsMaps
from atframework.web.common.maps.bo.bo_rebate_elements_maps import BoRebateElementsMaps
from atframework.web.common.maps.bo.bo_voucher_elements_maps import BoVoucherElementsMaps
from atframework.web.common.maps.bo.bo_helpdesk_elements_maps import BoHelpdeskElementsMaps


class ElementsMaps(BoHeaderElementsMaps, BoLoginElementsMaps, BoRebateElementsMaps, BoVoucherElementsMaps,
                   BoHelpdeskElementsMaps):
    """
    Integrate all model to this class, Use this class to call elements
    """
