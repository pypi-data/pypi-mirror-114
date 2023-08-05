# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 1.8.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class GetManyCodeResponseDto(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'data': 'list[Code]',
        'count': 'float',
        'total': 'float',
        'page': 'float',
        'page_count': 'float'
    }

    attribute_map = {
        'data': 'data',
        'count': 'count',
        'total': 'total',
        'page': 'page',
        'page_count': 'pageCount'
    }

    def __init__(self, data=None, count=None, total=None, page=None, page_count=None):  # noqa: E501
        """GetManyCodeResponseDto - a model defined in Swagger"""  # noqa: E501
        self._data = None
        self._count = None
        self._total = None
        self._page = None
        self._page_count = None
        self.discriminator = None
        self.data = data
        self.count = count
        self.total = total
        self.page = page
        self.page_count = page_count

    @property
    def data(self):
        """Gets the data of this GetManyCodeResponseDto.  # noqa: E501


        :return: The data of this GetManyCodeResponseDto.  # noqa: E501
        :rtype: list[Code]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this GetManyCodeResponseDto.


        :param data: The data of this GetManyCodeResponseDto.  # noqa: E501
        :type: list[Code]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data

    @property
    def count(self):
        """Gets the count of this GetManyCodeResponseDto.  # noqa: E501


        :return: The count of this GetManyCodeResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this GetManyCodeResponseDto.


        :param count: The count of this GetManyCodeResponseDto.  # noqa: E501
        :type: float
        """
        if count is None:
            raise ValueError("Invalid value for `count`, must not be `None`")  # noqa: E501

        self._count = count

    @property
    def total(self):
        """Gets the total of this GetManyCodeResponseDto.  # noqa: E501


        :return: The total of this GetManyCodeResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this GetManyCodeResponseDto.


        :param total: The total of this GetManyCodeResponseDto.  # noqa: E501
        :type: float
        """
        if total is None:
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

    @property
    def page(self):
        """Gets the page of this GetManyCodeResponseDto.  # noqa: E501


        :return: The page of this GetManyCodeResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this GetManyCodeResponseDto.


        :param page: The page of this GetManyCodeResponseDto.  # noqa: E501
        :type: float
        """
        if page is None:
            raise ValueError("Invalid value for `page`, must not be `None`")  # noqa: E501

        self._page = page

    @property
    def page_count(self):
        """Gets the page_count of this GetManyCodeResponseDto.  # noqa: E501


        :return: The page_count of this GetManyCodeResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        """Sets the page_count of this GetManyCodeResponseDto.


        :param page_count: The page_count of this GetManyCodeResponseDto.  # noqa: E501
        :type: float
        """
        if page_count is None:
            raise ValueError("Invalid value for `page_count`, must not be `None`")  # noqa: E501

        self._page_count = page_count

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(GetManyCodeResponseDto, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetManyCodeResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
