"""
    Firefly III API Client

    This is the Python client for Firefly III API  # noqa: E501

    The version of the OpenAPI document: 1.5.4
    Contact: james@firefly-iii.org
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from firefly_iii_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from firefly_iii_client.exceptions import ApiAttributeError



class Account(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('type',): {
            'ASSET': "asset",
            'EXPENSE': "expense",
            'IMPORT': "import",
            'REVENUE': "revenue",
            'CASH': "cash",
            'LIABILITY': "liability",
            'LIABILITIES': "liabilities",
            'INITIAL-BALANCE': "initial-balance",
            'RECONCILIATION': "reconciliation",
        },
        ('account_role',): {
            'None': None,
            'DEFAULTASSET': "defaultAsset",
            'SHAREDASSET': "sharedAsset",
            'SAVINGASSET': "savingAsset",
            'CCASSET': "ccAsset",
            'CASHWALLETASSET': "cashWalletAsset",
            'NULL': "null",
        },
        ('credit_card_type',): {
            'None': None,
            'MONTHLYFULL': "monthlyFull",
            'NULL': "null",
        },
        ('interest_period',): {
            'None': None,
            'WEEKLY': "weekly",
            'MONTHLY': "monthly",
            'QUARTERLY': "quarterly",
            'HALF-YEAR': "half-year",
            'YEARLY': "yearly",
            'NULL': "null",
        },
        ('liability_direction',): {
            'CREDIT': "credit",
            'DEBIT': "debit",
        },
        ('liability_type',): {
            'None': None,
            'LOAN': "loan",
            'DEBT': "debt",
            'MORTGAGE': "mortgage",
            'NULL': "null",
        },
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'name': (str,),  # noqa: E501
            'type': (str,),  # noqa: E501
            'account_number': (str, none_type,),  # noqa: E501
            'account_role': (str, none_type,),  # noqa: E501
            'active': (bool,),  # noqa: E501
            'bic': (str, none_type,),  # noqa: E501
            'created_at': (datetime,),  # noqa: E501
            'credit_card_type': (str, none_type,),  # noqa: E501
            'currency_code': (str,),  # noqa: E501
            'currency_decimal_places': (int,),  # noqa: E501
            'currency_id': (str,),  # noqa: E501
            'currency_symbol': (str,),  # noqa: E501
            'current_balance': (str,),  # noqa: E501
            'current_balance_date': (datetime,),  # noqa: E501
            'current_debt': (str,),  # noqa: E501
            'iban': (str, none_type,),  # noqa: E501
            'include_net_worth': (bool,),  # noqa: E501
            'interest': (str, none_type,),  # noqa: E501
            'interest_period': (str, none_type,),  # noqa: E501
            'latitude': (float, none_type,),  # noqa: E501
            'liability_direction': (str,),  # noqa: E501
            'liability_type': (str, none_type,),  # noqa: E501
            'longitude': (float, none_type,),  # noqa: E501
            'monthly_payment_date': (datetime, none_type,),  # noqa: E501
            'notes': (str, none_type,),  # noqa: E501
            'opening_balance': (str,),  # noqa: E501
            'opening_balance_date': (datetime, none_type,),  # noqa: E501
            'order': (int, none_type,),  # noqa: E501
            'updated_at': (datetime,),  # noqa: E501
            'virtual_balance': (str,),  # noqa: E501
            'zoom_level': (int, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'type': 'type',  # noqa: E501
        'account_number': 'account_number',  # noqa: E501
        'account_role': 'account_role',  # noqa: E501
        'active': 'active',  # noqa: E501
        'bic': 'bic',  # noqa: E501
        'created_at': 'created_at',  # noqa: E501
        'credit_card_type': 'credit_card_type',  # noqa: E501
        'currency_code': 'currency_code',  # noqa: E501
        'currency_decimal_places': 'currency_decimal_places',  # noqa: E501
        'currency_id': 'currency_id',  # noqa: E501
        'currency_symbol': 'currency_symbol',  # noqa: E501
        'current_balance': 'current_balance',  # noqa: E501
        'current_balance_date': 'current_balance_date',  # noqa: E501
        'current_debt': 'current_debt',  # noqa: E501
        'iban': 'iban',  # noqa: E501
        'include_net_worth': 'include_net_worth',  # noqa: E501
        'interest': 'interest',  # noqa: E501
        'interest_period': 'interest_period',  # noqa: E501
        'latitude': 'latitude',  # noqa: E501
        'liability_direction': 'liability_direction',  # noqa: E501
        'liability_type': 'liability_type',  # noqa: E501
        'longitude': 'longitude',  # noqa: E501
        'monthly_payment_date': 'monthly_payment_date',  # noqa: E501
        'notes': 'notes',  # noqa: E501
        'opening_balance': 'opening_balance',  # noqa: E501
        'opening_balance_date': 'opening_balance_date',  # noqa: E501
        'order': 'order',  # noqa: E501
        'updated_at': 'updated_at',  # noqa: E501
        'virtual_balance': 'virtual_balance',  # noqa: E501
        'zoom_level': 'zoom_level',  # noqa: E501
    }

    read_only_vars = {
        'created_at',  # noqa: E501
        'currency_decimal_places',  # noqa: E501
        'currency_symbol',  # noqa: E501
        'current_balance',  # noqa: E501
        'current_balance_date',  # noqa: E501
        'updated_at',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, name, type, *args, **kwargs):  # noqa: E501
        """Account - a model defined in OpenAPI

        Args:
            name (str):
            type (str): Can only be one one these account types. import, initial-balance and reconciliation cannot be set manually.

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            account_number (str, none_type): [optional]  # noqa: E501
            account_role (str, none_type): Is only mandatory when the type is asset.. [optional]  # noqa: E501
            active (bool): If omitted, defaults to true.. [optional]  # noqa: E501
            bic (str, none_type): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            credit_card_type (str, none_type): Mandatory when the account_role is ccAsset. Can only be monthlyFull or null.. [optional]  # noqa: E501
            currency_code (str): Use either currency_id or currency_code. Defaults to the user's default currency.. [optional]  # noqa: E501
            currency_decimal_places (int): [optional]  # noqa: E501
            currency_id (str): Use either currency_id or currency_code. Defaults to the user's default currency.. [optional]  # noqa: E501
            currency_symbol (str): [optional]  # noqa: E501
            current_balance (str): [optional]  # noqa: E501
            current_balance_date (datetime): [optional]  # noqa: E501
            current_debt (str): Represents the current debt for liabilities.. [optional]  # noqa: E501
            iban (str, none_type): [optional]  # noqa: E501
            include_net_worth (bool): If omitted, defaults to true.. [optional]  # noqa: E501
            interest (str, none_type): Mandatory when type is liability. Interest percentage.. [optional]  # noqa: E501
            interest_period (str, none_type): Mandatory when type is liability. Period over which the interest is calculated.. [optional]  # noqa: E501
            latitude (float, none_type): Latitude of the accounts's location, if applicable. Can be used to draw a map.. [optional]  # noqa: E501
            liability_direction (str): 'credit' indicates somebody owes you the liability. 'debit' Indicates you owe this debt yourself. Works only for liabiltiies.. [optional]  # noqa: E501
            liability_type (str, none_type): Mandatory when type is liability. Specifies the exact type.. [optional]  # noqa: E501
            longitude (float, none_type): Latitude of the accounts's location, if applicable. Can be used to draw a map.. [optional]  # noqa: E501
            monthly_payment_date (datetime, none_type): Mandatory when the account_role is ccAsset. Moment at which CC payment installments are asked for by the bank.. [optional]  # noqa: E501
            notes (str, none_type): [optional]  # noqa: E501
            opening_balance (str): Represents the opening balance, the initial amount this account holds.. [optional]  # noqa: E501
            opening_balance_date (datetime, none_type): Represents the date of the opening balance.. [optional]  # noqa: E501
            order (int, none_type): Order of the account. Is NULL if account is not asset or liability.. [optional]  # noqa: E501
            updated_at (datetime): [optional]  # noqa: E501
            virtual_balance (str): [optional]  # noqa: E501
            zoom_level (int, none_type): Zoom level for the map, if drawn. This to set the box right. Unfortunately this is a proprietary value because each map provider has different zoom levels.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.name = name
        self.type = type
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, name, type, *args, **kwargs):  # noqa: E501
        """Account - a model defined in OpenAPI

        Args:
            name (str):
            type (str): Can only be one one these account types. import, initial-balance and reconciliation cannot be set manually.

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            account_number (str, none_type): [optional]  # noqa: E501
            account_role (str, none_type): Is only mandatory when the type is asset.. [optional]  # noqa: E501
            active (bool): If omitted, defaults to true.. [optional]  # noqa: E501
            bic (str, none_type): [optional]  # noqa: E501
            created_at (datetime): [optional]  # noqa: E501
            credit_card_type (str, none_type): Mandatory when the account_role is ccAsset. Can only be monthlyFull or null.. [optional]  # noqa: E501
            currency_code (str): Use either currency_id or currency_code. Defaults to the user's default currency.. [optional]  # noqa: E501
            currency_decimal_places (int): [optional]  # noqa: E501
            currency_id (str): Use either currency_id or currency_code. Defaults to the user's default currency.. [optional]  # noqa: E501
            currency_symbol (str): [optional]  # noqa: E501
            current_balance (str): [optional]  # noqa: E501
            current_balance_date (datetime): [optional]  # noqa: E501
            current_debt (str): Represents the current debt for liabilities.. [optional]  # noqa: E501
            iban (str, none_type): [optional]  # noqa: E501
            include_net_worth (bool): If omitted, defaults to true.. [optional]  # noqa: E501
            interest (str, none_type): Mandatory when type is liability. Interest percentage.. [optional]  # noqa: E501
            interest_period (str, none_type): Mandatory when type is liability. Period over which the interest is calculated.. [optional]  # noqa: E501
            latitude (float, none_type): Latitude of the accounts's location, if applicable. Can be used to draw a map.. [optional]  # noqa: E501
            liability_direction (str): 'credit' indicates somebody owes you the liability. 'debit' Indicates you owe this debt yourself. Works only for liabiltiies.. [optional]  # noqa: E501
            liability_type (str, none_type): Mandatory when type is liability. Specifies the exact type.. [optional]  # noqa: E501
            longitude (float, none_type): Latitude of the accounts's location, if applicable. Can be used to draw a map.. [optional]  # noqa: E501
            monthly_payment_date (datetime, none_type): Mandatory when the account_role is ccAsset. Moment at which CC payment installments are asked for by the bank.. [optional]  # noqa: E501
            notes (str, none_type): [optional]  # noqa: E501
            opening_balance (str): Represents the opening balance, the initial amount this account holds.. [optional]  # noqa: E501
            opening_balance_date (datetime, none_type): Represents the date of the opening balance.. [optional]  # noqa: E501
            order (int, none_type): Order of the account. Is NULL if account is not asset or liability.. [optional]  # noqa: E501
            updated_at (datetime): [optional]  # noqa: E501
            virtual_balance (str): [optional]  # noqa: E501
            zoom_level (int, none_type): Zoom level for the map, if drawn. This to set the box right. Unfortunately this is a proprietary value because each map provider has different zoom levels.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.name = name
        self.type = type
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
