# coding: utf-8

"""
    Firefly III API Client

    This is the Python client for Firefly III API  # noqa: E501

    The version of the OpenAPI document: 0.10.0
    Contact: thegrumpydictator@gmail.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class RuleActionUpdate(object):
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
        'active': 'bool',
        'stop_processing': 'bool',
        'type': 'str',
        'value': 'str'
    }

    attribute_map = {
        'active': 'active',
        'stop_processing': 'stop_processing',
        'type': 'type',
        'value': 'value'
    }

    def __init__(self, active=None, stop_processing=None, type=None, value=None):  # noqa: E501
        """RuleActionUpdate - a model defined in OpenAPI"""  # noqa: E501

        self._active = None
        self._stop_processing = None
        self._type = None
        self._value = None
        self.discriminator = None

        if active is not None:
            self.active = active
        if stop_processing is not None:
            self.stop_processing = stop_processing
        self.type = type
        self.value = value

    @property
    def active(self):
        """Gets the active of this RuleActionUpdate.  # noqa: E501

        If the action is active.  # noqa: E501

        :return: The active of this RuleActionUpdate.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this RuleActionUpdate.

        If the action is active.  # noqa: E501

        :param active: The active of this RuleActionUpdate.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def stop_processing(self):
        """Gets the stop_processing of this RuleActionUpdate.  # noqa: E501

        When true, other actions will not be fired after this action has fired.  # noqa: E501

        :return: The stop_processing of this RuleActionUpdate.  # noqa: E501
        :rtype: bool
        """
        return self._stop_processing

    @stop_processing.setter
    def stop_processing(self, stop_processing):
        """Sets the stop_processing of this RuleActionUpdate.

        When true, other actions will not be fired after this action has fired.  # noqa: E501

        :param stop_processing: The stop_processing of this RuleActionUpdate.  # noqa: E501
        :type: bool
        """

        self._stop_processing = stop_processing

    @property
    def type(self):
        """Gets the type of this RuleActionUpdate.  # noqa: E501

        The type of thing this action will do. A limited set is possible.  # noqa: E501

        :return: The type of this RuleActionUpdate.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this RuleActionUpdate.

        The type of thing this action will do. A limited set is possible.  # noqa: E501

        :param type: The type of this RuleActionUpdate.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["user_action", "set_category", "clear_category", "set_budget", "clear_budget", "add_tag", "remove_tag", "remove_all_tags", "set_description", "append_description", "prepend_description", "aet_source_account", "set_destination_account", "set_notes", "append_notes", "prepend_notes", "clear_notes", "link_to_bill", "convert_withdrawal", "convert_deposit", "convert_transfer"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def value(self):
        """Gets the value of this RuleActionUpdate.  # noqa: E501

        The accompanying value the action will set, change or update. Can be empty, but for some types this value is mandatory.  # noqa: E501

        :return: The value of this RuleActionUpdate.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this RuleActionUpdate.

        The accompanying value the action will set, change or update. Can be empty, but for some types this value is mandatory.  # noqa: E501

        :param value: The value of this RuleActionUpdate.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if not isinstance(other, RuleActionUpdate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
