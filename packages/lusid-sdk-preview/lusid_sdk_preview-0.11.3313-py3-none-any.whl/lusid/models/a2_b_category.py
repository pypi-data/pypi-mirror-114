# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3313
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class A2BCategory(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'holding_currency': 'A2BBreakdown',
        'portfolio_currency': 'A2BBreakdown'
    }

    attribute_map = {
        'holding_currency': 'holdingCurrency',
        'portfolio_currency': 'portfolioCurrency'
    }

    required_map = {
        'holding_currency': 'optional',
        'portfolio_currency': 'optional'
    }

    def __init__(self, holding_currency=None, portfolio_currency=None):  # noqa: E501
        """
        A2BCategory - a model defined in OpenAPI

        :param holding_currency: 
        :type holding_currency: lusid.A2BBreakdown
        :param portfolio_currency: 
        :type portfolio_currency: lusid.A2BBreakdown

        """  # noqa: E501

        self._holding_currency = None
        self._portfolio_currency = None
        self.discriminator = None

        if holding_currency is not None:
            self.holding_currency = holding_currency
        if portfolio_currency is not None:
            self.portfolio_currency = portfolio_currency

    @property
    def holding_currency(self):
        """Gets the holding_currency of this A2BCategory.  # noqa: E501


        :return: The holding_currency of this A2BCategory.  # noqa: E501
        :rtype: A2BBreakdown
        """
        return self._holding_currency

    @holding_currency.setter
    def holding_currency(self, holding_currency):
        """Sets the holding_currency of this A2BCategory.


        :param holding_currency: The holding_currency of this A2BCategory.  # noqa: E501
        :type: A2BBreakdown
        """

        self._holding_currency = holding_currency

    @property
    def portfolio_currency(self):
        """Gets the portfolio_currency of this A2BCategory.  # noqa: E501


        :return: The portfolio_currency of this A2BCategory.  # noqa: E501
        :rtype: A2BBreakdown
        """
        return self._portfolio_currency

    @portfolio_currency.setter
    def portfolio_currency(self, portfolio_currency):
        """Sets the portfolio_currency of this A2BCategory.


        :param portfolio_currency: The portfolio_currency of this A2BCategory.  # noqa: E501
        :type: A2BBreakdown
        """

        self._portfolio_currency = portfolio_currency

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, A2BCategory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
