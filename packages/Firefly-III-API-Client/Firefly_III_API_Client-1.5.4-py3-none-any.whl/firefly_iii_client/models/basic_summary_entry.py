# coding: utf-8

"""
    Firefly III API Client

    This is the Python client for Firefly III API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Contact: james@firefly-iii.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from firefly_iii_client.configuration import Configuration


class BasicSummaryEntry(object):
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
    """
    openapi_types = {
        'currency_code': 'str',
        'currency_decimal_places': 'int',
        'currency_id': 'int',
        'currency_symbol': 'str',
        'key': 'str',
        'local_icon': 'str',
        'monetary_value': 'float',
        'sub_title': 'str',
        'title': 'str',
        'value_parsed': 'str'
    }

    attribute_map = {
        'currency_code': 'currency_code',
        'currency_decimal_places': 'currency_decimal_places',
        'currency_id': 'currency_id',
        'currency_symbol': 'currency_symbol',
        'key': 'key',
        'local_icon': 'local_icon',
        'monetary_value': 'monetary_value',
        'sub_title': 'sub_title',
        'title': 'title',
        'value_parsed': 'value_parsed'
    }

    def __init__(self, currency_code=None, currency_decimal_places=None, currency_id=None, currency_symbol=None, key=None, local_icon=None, monetary_value=None, sub_title=None, title=None, value_parsed=None, local_vars_configuration=None):  # noqa: E501
        """BasicSummaryEntry - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._currency_code = None
        self._currency_decimal_places = None
        self._currency_id = None
        self._currency_symbol = None
        self._key = None
        self._local_icon = None
        self._monetary_value = None
        self._sub_title = None
        self._title = None
        self._value_parsed = None
        self.discriminator = None

        if currency_code is not None:
            self.currency_code = currency_code
        if currency_decimal_places is not None:
            self.currency_decimal_places = currency_decimal_places
        if currency_id is not None:
            self.currency_id = currency_id
        if currency_symbol is not None:
            self.currency_symbol = currency_symbol
        if key is not None:
            self.key = key
        if local_icon is not None:
            self.local_icon = local_icon
        if monetary_value is not None:
            self.monetary_value = monetary_value
        if sub_title is not None:
            self.sub_title = sub_title
        if title is not None:
            self.title = title
        if value_parsed is not None:
            self.value_parsed = value_parsed

    @property
    def currency_code(self):
        """Gets the currency_code of this BasicSummaryEntry.  # noqa: E501


        :return: The currency_code of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """Sets the currency_code of this BasicSummaryEntry.


        :param currency_code: The currency_code of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._currency_code = currency_code

    @property
    def currency_decimal_places(self):
        """Gets the currency_decimal_places of this BasicSummaryEntry.  # noqa: E501

        Number of decimals for the associated currency.  # noqa: E501

        :return: The currency_decimal_places of this BasicSummaryEntry.  # noqa: E501
        :rtype: int
        """
        return self._currency_decimal_places

    @currency_decimal_places.setter
    def currency_decimal_places(self, currency_decimal_places):
        """Sets the currency_decimal_places of this BasicSummaryEntry.

        Number of decimals for the associated currency.  # noqa: E501

        :param currency_decimal_places: The currency_decimal_places of this BasicSummaryEntry.  # noqa: E501
        :type: int
        """

        self._currency_decimal_places = currency_decimal_places

    @property
    def currency_id(self):
        """Gets the currency_id of this BasicSummaryEntry.  # noqa: E501

        The currency ID of the associated currency.  # noqa: E501

        :return: The currency_id of this BasicSummaryEntry.  # noqa: E501
        :rtype: int
        """
        return self._currency_id

    @currency_id.setter
    def currency_id(self, currency_id):
        """Sets the currency_id of this BasicSummaryEntry.

        The currency ID of the associated currency.  # noqa: E501

        :param currency_id: The currency_id of this BasicSummaryEntry.  # noqa: E501
        :type: int
        """

        self._currency_id = currency_id

    @property
    def currency_symbol(self):
        """Gets the currency_symbol of this BasicSummaryEntry.  # noqa: E501


        :return: The currency_symbol of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._currency_symbol

    @currency_symbol.setter
    def currency_symbol(self, currency_symbol):
        """Sets the currency_symbol of this BasicSummaryEntry.


        :param currency_symbol: The currency_symbol of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._currency_symbol = currency_symbol

    @property
    def key(self):
        """Gets the key of this BasicSummaryEntry.  # noqa: E501

        This is a reference to the type of info shared, not influenced by translations or user preferences.  # noqa: E501

        :return: The key of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this BasicSummaryEntry.

        This is a reference to the type of info shared, not influenced by translations or user preferences.  # noqa: E501

        :param key: The key of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def local_icon(self):
        """Gets the local_icon of this BasicSummaryEntry.  # noqa: E501

        Reference to a font-awesome icon without the fa- part.  # noqa: E501

        :return: The local_icon of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._local_icon

    @local_icon.setter
    def local_icon(self, local_icon):
        """Sets the local_icon of this BasicSummaryEntry.

        Reference to a font-awesome icon without the fa- part.  # noqa: E501

        :param local_icon: The local_icon of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._local_icon = local_icon

    @property
    def monetary_value(self):
        """Gets the monetary_value of this BasicSummaryEntry.  # noqa: E501

        The amount as a float.  # noqa: E501

        :return: The monetary_value of this BasicSummaryEntry.  # noqa: E501
        :rtype: float
        """
        return self._monetary_value

    @monetary_value.setter
    def monetary_value(self, monetary_value):
        """Sets the monetary_value of this BasicSummaryEntry.

        The amount as a float.  # noqa: E501

        :param monetary_value: The monetary_value of this BasicSummaryEntry.  # noqa: E501
        :type: float
        """

        self._monetary_value = monetary_value

    @property
    def sub_title(self):
        """Gets the sub_title of this BasicSummaryEntry.  # noqa: E501

        A short explanation of the amounts origin. Already formatted according to the locale of the user or translated, if relevant.  # noqa: E501

        :return: The sub_title of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._sub_title

    @sub_title.setter
    def sub_title(self, sub_title):
        """Sets the sub_title of this BasicSummaryEntry.

        A short explanation of the amounts origin. Already formatted according to the locale of the user or translated, if relevant.  # noqa: E501

        :param sub_title: The sub_title of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._sub_title = sub_title

    @property
    def title(self):
        """Gets the title of this BasicSummaryEntry.  # noqa: E501

        A translated title for the information shared.  # noqa: E501

        :return: The title of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this BasicSummaryEntry.

        A translated title for the information shared.  # noqa: E501

        :param title: The title of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def value_parsed(self):
        """Gets the value_parsed of this BasicSummaryEntry.  # noqa: E501

        The amount formatted according to the users locale  # noqa: E501

        :return: The value_parsed of this BasicSummaryEntry.  # noqa: E501
        :rtype: str
        """
        return self._value_parsed

    @value_parsed.setter
    def value_parsed(self, value_parsed):
        """Sets the value_parsed of this BasicSummaryEntry.

        The amount formatted according to the users locale  # noqa: E501

        :param value_parsed: The value_parsed of this BasicSummaryEntry.  # noqa: E501
        :type: str
        """

        self._value_parsed = value_parsed

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
        if not isinstance(other, BasicSummaryEntry):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BasicSummaryEntry):
            return True

        return self.to_dict() != other.to_dict()
