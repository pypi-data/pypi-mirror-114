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

class PlacementSetRequest(object):
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
        'requests': 'list[PlacementRequest]'
    }

    attribute_map = {
        'requests': 'requests'
    }

    required_map = {
        'requests': 'optional'
    }

    def __init__(self, requests=None):  # noqa: E501
        """
        PlacementSetRequest - a model defined in OpenAPI

        :param requests:  A collection of PlacementRequests.
        :type requests: list[lusid.PlacementRequest]

        """  # noqa: E501

        self._requests = None
        self.discriminator = None

        self.requests = requests

    @property
    def requests(self):
        """Gets the requests of this PlacementSetRequest.  # noqa: E501

        A collection of PlacementRequests.  # noqa: E501

        :return: The requests of this PlacementSetRequest.  # noqa: E501
        :rtype: list[PlacementRequest]
        """
        return self._requests

    @requests.setter
    def requests(self, requests):
        """Sets the requests of this PlacementSetRequest.

        A collection of PlacementRequests.  # noqa: E501

        :param requests: The requests of this PlacementSetRequest.  # noqa: E501
        :type: list[PlacementRequest]
        """

        self._requests = requests

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
        if not isinstance(other, PlacementSetRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
