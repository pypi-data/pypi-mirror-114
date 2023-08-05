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

class DiscountFactorCurveData(object):
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
        'base_date': 'datetime',
        'dates': 'list[datetime]',
        'discount_factors': 'list[float]',
        'market_data_type': 'str'
    }

    attribute_map = {
        'base_date': 'baseDate',
        'dates': 'dates',
        'discount_factors': 'discountFactors',
        'market_data_type': 'marketDataType'
    }

    required_map = {
        'base_date': 'required',
        'dates': 'required',
        'discount_factors': 'required',
        'market_data_type': 'required'
    }

    def __init__(self, base_date=None, dates=None, discount_factors=None, market_data_type=None):  # noqa: E501
        """
        DiscountFactorCurveData - a model defined in OpenAPI

        :param base_date:  BaseDate for the Curve (required)
        :type base_date: datetime
        :param dates:  Dates for which the discount factors apply (required)
        :type dates: list[datetime]
        :param discount_factors:  Discount factors to be applied to cashflow on the specified dates (required)
        :type discount_factors: list[float]
        :param market_data_type:  The available values are: DiscountFactorCurveData, EquityVolSurfaceData, FxVolSurfaceData, IrVolCubeData, OpaqueMarketData, YieldCurveData (required)
        :type market_data_type: str

        """  # noqa: E501

        self._base_date = None
        self._dates = None
        self._discount_factors = None
        self._market_data_type = None
        self.discriminator = None

        self.base_date = base_date
        self.dates = dates
        self.discount_factors = discount_factors
        self.market_data_type = market_data_type

    @property
    def base_date(self):
        """Gets the base_date of this DiscountFactorCurveData.  # noqa: E501

        BaseDate for the Curve  # noqa: E501

        :return: The base_date of this DiscountFactorCurveData.  # noqa: E501
        :rtype: datetime
        """
        return self._base_date

    @base_date.setter
    def base_date(self, base_date):
        """Sets the base_date of this DiscountFactorCurveData.

        BaseDate for the Curve  # noqa: E501

        :param base_date: The base_date of this DiscountFactorCurveData.  # noqa: E501
        :type: datetime
        """
        if base_date is None:
            raise ValueError("Invalid value for `base_date`, must not be `None`")  # noqa: E501

        self._base_date = base_date

    @property
    def dates(self):
        """Gets the dates of this DiscountFactorCurveData.  # noqa: E501

        Dates for which the discount factors apply  # noqa: E501

        :return: The dates of this DiscountFactorCurveData.  # noqa: E501
        :rtype: list[datetime]
        """
        return self._dates

    @dates.setter
    def dates(self, dates):
        """Sets the dates of this DiscountFactorCurveData.

        Dates for which the discount factors apply  # noqa: E501

        :param dates: The dates of this DiscountFactorCurveData.  # noqa: E501
        :type: list[datetime]
        """
        if dates is None:
            raise ValueError("Invalid value for `dates`, must not be `None`")  # noqa: E501

        self._dates = dates

    @property
    def discount_factors(self):
        """Gets the discount_factors of this DiscountFactorCurveData.  # noqa: E501

        Discount factors to be applied to cashflow on the specified dates  # noqa: E501

        :return: The discount_factors of this DiscountFactorCurveData.  # noqa: E501
        :rtype: list[float]
        """
        return self._discount_factors

    @discount_factors.setter
    def discount_factors(self, discount_factors):
        """Sets the discount_factors of this DiscountFactorCurveData.

        Discount factors to be applied to cashflow on the specified dates  # noqa: E501

        :param discount_factors: The discount_factors of this DiscountFactorCurveData.  # noqa: E501
        :type: list[float]
        """
        if discount_factors is None:
            raise ValueError("Invalid value for `discount_factors`, must not be `None`")  # noqa: E501

        self._discount_factors = discount_factors

    @property
    def market_data_type(self):
        """Gets the market_data_type of this DiscountFactorCurveData.  # noqa: E501

        The available values are: DiscountFactorCurveData, EquityVolSurfaceData, FxVolSurfaceData, IrVolCubeData, OpaqueMarketData, YieldCurveData  # noqa: E501

        :return: The market_data_type of this DiscountFactorCurveData.  # noqa: E501
        :rtype: str
        """
        return self._market_data_type

    @market_data_type.setter
    def market_data_type(self, market_data_type):
        """Sets the market_data_type of this DiscountFactorCurveData.

        The available values are: DiscountFactorCurveData, EquityVolSurfaceData, FxVolSurfaceData, IrVolCubeData, OpaqueMarketData, YieldCurveData  # noqa: E501

        :param market_data_type: The market_data_type of this DiscountFactorCurveData.  # noqa: E501
        :type: str
        """
        if market_data_type is None:
            raise ValueError("Invalid value for `market_data_type`, must not be `None`")  # noqa: E501
        allowed_values = ["DiscountFactorCurveData", "EquityVolSurfaceData", "FxVolSurfaceData", "IrVolCubeData", "OpaqueMarketData", "YieldCurveData"]  # noqa: E501
        if market_data_type not in allowed_values:
            raise ValueError(
                "Invalid value for `market_data_type` ({0}), must be one of {1}"  # noqa: E501
                .format(market_data_type, allowed_values)
            )

        self._market_data_type = market_data_type

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
        if not isinstance(other, DiscountFactorCurveData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
