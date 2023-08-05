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

class Organization(object):
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
        'id': 'str',
        'name': 'str',
        'instance_url': 'str',
        'domain': 'str',
        'datasets': 'list[str]',
        'projects': 'list[str]',
        'organization_settings': 'list[str]',
        'organization_feature_exclusions': 'list[str]',
        'organization_feature_category_exclusions': 'list[str]',
        'last_updated_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'instance_url': 'instanceUrl',
        'domain': 'domain',
        'datasets': 'datasets',
        'projects': 'projects',
        'organization_settings': 'organizationSettings',
        'organization_feature_exclusions': 'organizationFeatureExclusions',
        'organization_feature_category_exclusions': 'organizationFeatureCategoryExclusions',
        'last_updated_by': 'lastUpdatedBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, instance_url=None, domain=None, datasets=None, projects=None, organization_settings=None, organization_feature_exclusions=None, organization_feature_category_exclusions=None, last_updated_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Organization - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._instance_url = None
        self._domain = None
        self._datasets = None
        self._projects = None
        self._organization_settings = None
        self._organization_feature_exclusions = None
        self._organization_feature_category_exclusions = None
        self._last_updated_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        self.instance_url = instance_url
        self.domain = domain
        if datasets is not None:
            self.datasets = datasets
        if projects is not None:
            self.projects = projects
        if organization_settings is not None:
            self.organization_settings = organization_settings
        if organization_feature_exclusions is not None:
            self.organization_feature_exclusions = organization_feature_exclusions
        if organization_feature_category_exclusions is not None:
            self.organization_feature_category_exclusions = organization_feature_category_exclusions
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this Organization.  # noqa: E501


        :return: The id of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Organization.


        :param id: The id of this Organization.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Organization.  # noqa: E501


        :return: The name of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Organization.


        :param name: The name of this Organization.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def instance_url(self):
        """Gets the instance_url of this Organization.  # noqa: E501


        :return: The instance_url of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._instance_url

    @instance_url.setter
    def instance_url(self, instance_url):
        """Sets the instance_url of this Organization.


        :param instance_url: The instance_url of this Organization.  # noqa: E501
        :type: str
        """
        if instance_url is None:
            raise ValueError("Invalid value for `instance_url`, must not be `None`")  # noqa: E501

        self._instance_url = instance_url

    @property
    def domain(self):
        """Gets the domain of this Organization.  # noqa: E501


        :return: The domain of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this Organization.


        :param domain: The domain of this Organization.  # noqa: E501
        :type: str
        """
        if domain is None:
            raise ValueError("Invalid value for `domain`, must not be `None`")  # noqa: E501

        self._domain = domain

    @property
    def datasets(self):
        """Gets the datasets of this Organization.  # noqa: E501


        :return: The datasets of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._datasets

    @datasets.setter
    def datasets(self, datasets):
        """Sets the datasets of this Organization.


        :param datasets: The datasets of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._datasets = datasets

    @property
    def projects(self):
        """Gets the projects of this Organization.  # noqa: E501


        :return: The projects of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._projects

    @projects.setter
    def projects(self, projects):
        """Sets the projects of this Organization.


        :param projects: The projects of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._projects = projects

    @property
    def organization_settings(self):
        """Gets the organization_settings of this Organization.  # noqa: E501


        :return: The organization_settings of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._organization_settings

    @organization_settings.setter
    def organization_settings(self, organization_settings):
        """Sets the organization_settings of this Organization.


        :param organization_settings: The organization_settings of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._organization_settings = organization_settings

    @property
    def organization_feature_exclusions(self):
        """Gets the organization_feature_exclusions of this Organization.  # noqa: E501


        :return: The organization_feature_exclusions of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._organization_feature_exclusions

    @organization_feature_exclusions.setter
    def organization_feature_exclusions(self, organization_feature_exclusions):
        """Sets the organization_feature_exclusions of this Organization.


        :param organization_feature_exclusions: The organization_feature_exclusions of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._organization_feature_exclusions = organization_feature_exclusions

    @property
    def organization_feature_category_exclusions(self):
        """Gets the organization_feature_category_exclusions of this Organization.  # noqa: E501


        :return: The organization_feature_category_exclusions of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._organization_feature_category_exclusions

    @organization_feature_category_exclusions.setter
    def organization_feature_category_exclusions(self, organization_feature_category_exclusions):
        """Sets the organization_feature_category_exclusions of this Organization.


        :param organization_feature_category_exclusions: The organization_feature_category_exclusions of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._organization_feature_category_exclusions = organization_feature_category_exclusions

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Organization.  # noqa: E501


        :return: The last_updated_by of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Organization.


        :param last_updated_by: The last_updated_by of this Organization.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_at(self):
        """Gets the created_at of this Organization.  # noqa: E501


        :return: The created_at of this Organization.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Organization.


        :param created_at: The created_at of this Organization.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Organization.  # noqa: E501


        :return: The updated_at of this Organization.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Organization.


        :param updated_at: The updated_at of this Organization.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Organization.  # noqa: E501


        :return: The version of this Organization.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Organization.


        :param version: The version of this Organization.  # noqa: E501
        :type: float
        """

        self._version = version

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
        if issubclass(Organization, dict):
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
        if not isinstance(other, Organization):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
