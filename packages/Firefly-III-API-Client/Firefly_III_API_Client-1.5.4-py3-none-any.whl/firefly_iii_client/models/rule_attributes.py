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


class RuleAttributes(object):
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
        'actions': 'list[RuleAction]',
        'active': 'bool',
        'created_at': 'datetime',
        'description': 'str',
        'order': 'int',
        'rule_group_id': 'int',
        'stop_processing': 'bool',
        'strict': 'bool',
        'title': 'str',
        'triggers': 'list[RuleTrigger]',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'actions': 'actions',
        'active': 'active',
        'created_at': 'created_at',
        'description': 'description',
        'order': 'order',
        'rule_group_id': 'rule_group_id',
        'stop_processing': 'stop_processing',
        'strict': 'strict',
        'title': 'title',
        'triggers': 'triggers',
        'updated_at': 'updated_at'
    }

    def __init__(self, actions=None, active=None, created_at=None, description=None, order=None, rule_group_id=None, stop_processing=None, strict=None, title=None, triggers=None, updated_at=None):  # noqa: E501
        """RuleAttributes - a model defined in OpenAPI"""  # noqa: E501

        self._actions = None
        self._active = None
        self._created_at = None
        self._description = None
        self._order = None
        self._rule_group_id = None
        self._stop_processing = None
        self._strict = None
        self._title = None
        self._triggers = None
        self._updated_at = None
        self.discriminator = None

        if actions is not None:
            self.actions = actions
        if active is not None:
            self.active = active
        if created_at is not None:
            self.created_at = created_at
        if description is not None:
            self.description = description
        if order is not None:
            self.order = order
        if rule_group_id is not None:
            self.rule_group_id = rule_group_id
        if stop_processing is not None:
            self.stop_processing = stop_processing
        if strict is not None:
            self.strict = strict
        if title is not None:
            self.title = title
        if triggers is not None:
            self.triggers = triggers
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def actions(self):
        """Gets the actions of this RuleAttributes.  # noqa: E501


        :return: The actions of this RuleAttributes.  # noqa: E501
        :rtype: list[RuleAction]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this RuleAttributes.


        :param actions: The actions of this RuleAttributes.  # noqa: E501
        :type: list[RuleAction]
        """

        self._actions = actions

    @property
    def active(self):
        """Gets the active of this RuleAttributes.  # noqa: E501


        :return: The active of this RuleAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this RuleAttributes.


        :param active: The active of this RuleAttributes.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def created_at(self):
        """Gets the created_at of this RuleAttributes.  # noqa: E501


        :return: The created_at of this RuleAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this RuleAttributes.


        :param created_at: The created_at of this RuleAttributes.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def description(self):
        """Gets the description of this RuleAttributes.  # noqa: E501


        :return: The description of this RuleAttributes.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RuleAttributes.


        :param description: The description of this RuleAttributes.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def order(self):
        """Gets the order of this RuleAttributes.  # noqa: E501


        :return: The order of this RuleAttributes.  # noqa: E501
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this RuleAttributes.


        :param order: The order of this RuleAttributes.  # noqa: E501
        :type: int
        """

        self._order = order

    @property
    def rule_group_id(self):
        """Gets the rule_group_id of this RuleAttributes.  # noqa: E501

        Reference to the rule group of which this rule is a part.  # noqa: E501

        :return: The rule_group_id of this RuleAttributes.  # noqa: E501
        :rtype: int
        """
        return self._rule_group_id

    @rule_group_id.setter
    def rule_group_id(self, rule_group_id):
        """Sets the rule_group_id of this RuleAttributes.

        Reference to the rule group of which this rule is a part.  # noqa: E501

        :param rule_group_id: The rule_group_id of this RuleAttributes.  # noqa: E501
        :type: int
        """

        self._rule_group_id = rule_group_id

    @property
    def stop_processing(self):
        """Gets the stop_processing of this RuleAttributes.  # noqa: E501

        If set to true, other rules in this group will not fire if this rule has fired.  # noqa: E501

        :return: The stop_processing of this RuleAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._stop_processing

    @stop_processing.setter
    def stop_processing(self, stop_processing):
        """Sets the stop_processing of this RuleAttributes.

        If set to true, other rules in this group will not fire if this rule has fired.  # noqa: E501

        :param stop_processing: The stop_processing of this RuleAttributes.  # noqa: E501
        :type: bool
        """

        self._stop_processing = stop_processing

    @property
    def strict(self):
        """Gets the strict of this RuleAttributes.  # noqa: E501

        When the rule is strict, ALL triggers must be triggerd for the actions to fire. If not, one is enough.  # noqa: E501

        :return: The strict of this RuleAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._strict

    @strict.setter
    def strict(self, strict):
        """Sets the strict of this RuleAttributes.

        When the rule is strict, ALL triggers must be triggerd for the actions to fire. If not, one is enough.  # noqa: E501

        :param strict: The strict of this RuleAttributes.  # noqa: E501
        :type: bool
        """

        self._strict = strict

    @property
    def title(self):
        """Gets the title of this RuleAttributes.  # noqa: E501


        :return: The title of this RuleAttributes.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this RuleAttributes.


        :param title: The title of this RuleAttributes.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def triggers(self):
        """Gets the triggers of this RuleAttributes.  # noqa: E501


        :return: The triggers of this RuleAttributes.  # noqa: E501
        :rtype: list[RuleTrigger]
        """
        return self._triggers

    @triggers.setter
    def triggers(self, triggers):
        """Sets the triggers of this RuleAttributes.


        :param triggers: The triggers of this RuleAttributes.  # noqa: E501
        :type: list[RuleTrigger]
        """

        self._triggers = triggers

    @property
    def updated_at(self):
        """Gets the updated_at of this RuleAttributes.  # noqa: E501


        :return: The updated_at of this RuleAttributes.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this RuleAttributes.


        :param updated_at: The updated_at of this RuleAttributes.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

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
        if not isinstance(other, RuleAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
