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

class Feature(object):
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
        'column_name': 'str',
        'column_alias': 'str',
        'display_name': 'str',
        'feature_sub_category_id': 'str',
        'aggregation_type': 'str',
        'is_filter': 'bool',
        'is_trainable': 'bool',
        'is_explainable': 'bool',
        'is_categorical': 'bool',
        'category_values': 'object',
        'type': 'str',
        'feature_table_id': 'str',
        'feature_table': 'FeatureTable',
        'feature_sub_category': 'FeatureSubCategory',
        'model_job_output_features': 'list[ModelJobOutputFeature]',
        'organization_feature_exclusions': 'list[OrganizationFeatureExclusion]',
        'last_updated_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'column_name': 'columnName',
        'column_alias': 'columnAlias',
        'display_name': 'displayName',
        'feature_sub_category_id': 'featureSubCategoryId',
        'aggregation_type': 'aggregationType',
        'is_filter': 'isFilter',
        'is_trainable': 'isTrainable',
        'is_explainable': 'isExplainable',
        'is_categorical': 'isCategorical',
        'category_values': 'categoryValues',
        'type': 'type',
        'feature_table_id': 'featureTableId',
        'feature_table': 'featureTable',
        'feature_sub_category': 'featureSubCategory',
        'model_job_output_features': 'modelJobOutputFeatures',
        'organization_feature_exclusions': 'organizationFeatureExclusions',
        'last_updated_by': 'lastUpdatedBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, column_name=None, column_alias=None, display_name=None, feature_sub_category_id=None, aggregation_type=None, is_filter=None, is_trainable=None, is_explainable=None, is_categorical=None, category_values=None, type=None, feature_table_id=None, feature_table=None, feature_sub_category=None, model_job_output_features=None, organization_feature_exclusions=None, last_updated_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Feature - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._column_name = None
        self._column_alias = None
        self._display_name = None
        self._feature_sub_category_id = None
        self._aggregation_type = None
        self._is_filter = None
        self._is_trainable = None
        self._is_explainable = None
        self._is_categorical = None
        self._category_values = None
        self._type = None
        self._feature_table_id = None
        self._feature_table = None
        self._feature_sub_category = None
        self._model_job_output_features = None
        self._organization_feature_exclusions = None
        self._last_updated_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.column_name = column_name
        self.column_alias = column_alias
        self.display_name = display_name
        self.feature_sub_category_id = feature_sub_category_id
        self.aggregation_type = aggregation_type
        self.is_filter = is_filter
        self.is_trainable = is_trainable
        self.is_explainable = is_explainable
        self.is_categorical = is_categorical
        if category_values is not None:
            self.category_values = category_values
        self.type = type
        self.feature_table_id = feature_table_id
        if feature_table is not None:
            self.feature_table = feature_table
        if feature_sub_category is not None:
            self.feature_sub_category = feature_sub_category
        if model_job_output_features is not None:
            self.model_job_output_features = model_job_output_features
        if organization_feature_exclusions is not None:
            self.organization_feature_exclusions = organization_feature_exclusions
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
        """Gets the id of this Feature.  # noqa: E501


        :return: The id of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Feature.


        :param id: The id of this Feature.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def column_name(self):
        """Gets the column_name of this Feature.  # noqa: E501


        :return: The column_name of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._column_name

    @column_name.setter
    def column_name(self, column_name):
        """Sets the column_name of this Feature.


        :param column_name: The column_name of this Feature.  # noqa: E501
        :type: str
        """
        if column_name is None:
            raise ValueError("Invalid value for `column_name`, must not be `None`")  # noqa: E501

        self._column_name = column_name

    @property
    def column_alias(self):
        """Gets the column_alias of this Feature.  # noqa: E501


        :return: The column_alias of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._column_alias

    @column_alias.setter
    def column_alias(self, column_alias):
        """Sets the column_alias of this Feature.


        :param column_alias: The column_alias of this Feature.  # noqa: E501
        :type: str
        """
        if column_alias is None:
            raise ValueError("Invalid value for `column_alias`, must not be `None`")  # noqa: E501

        self._column_alias = column_alias

    @property
    def display_name(self):
        """Gets the display_name of this Feature.  # noqa: E501


        :return: The display_name of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this Feature.


        :param display_name: The display_name of this Feature.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def feature_sub_category_id(self):
        """Gets the feature_sub_category_id of this Feature.  # noqa: E501


        :return: The feature_sub_category_id of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._feature_sub_category_id

    @feature_sub_category_id.setter
    def feature_sub_category_id(self, feature_sub_category_id):
        """Sets the feature_sub_category_id of this Feature.


        :param feature_sub_category_id: The feature_sub_category_id of this Feature.  # noqa: E501
        :type: str
        """
        if feature_sub_category_id is None:
            raise ValueError("Invalid value for `feature_sub_category_id`, must not be `None`")  # noqa: E501

        self._feature_sub_category_id = feature_sub_category_id

    @property
    def aggregation_type(self):
        """Gets the aggregation_type of this Feature.  # noqa: E501


        :return: The aggregation_type of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """Sets the aggregation_type of this Feature.


        :param aggregation_type: The aggregation_type of this Feature.  # noqa: E501
        :type: str
        """
        if aggregation_type is None:
            raise ValueError("Invalid value for `aggregation_type`, must not be `None`")  # noqa: E501

        self._aggregation_type = aggregation_type

    @property
    def is_filter(self):
        """Gets the is_filter of this Feature.  # noqa: E501


        :return: The is_filter of this Feature.  # noqa: E501
        :rtype: bool
        """
        return self._is_filter

    @is_filter.setter
    def is_filter(self, is_filter):
        """Sets the is_filter of this Feature.


        :param is_filter: The is_filter of this Feature.  # noqa: E501
        :type: bool
        """
        if is_filter is None:
            raise ValueError("Invalid value for `is_filter`, must not be `None`")  # noqa: E501

        self._is_filter = is_filter

    @property
    def is_trainable(self):
        """Gets the is_trainable of this Feature.  # noqa: E501


        :return: The is_trainable of this Feature.  # noqa: E501
        :rtype: bool
        """
        return self._is_trainable

    @is_trainable.setter
    def is_trainable(self, is_trainable):
        """Sets the is_trainable of this Feature.


        :param is_trainable: The is_trainable of this Feature.  # noqa: E501
        :type: bool
        """
        if is_trainable is None:
            raise ValueError("Invalid value for `is_trainable`, must not be `None`")  # noqa: E501

        self._is_trainable = is_trainable

    @property
    def is_explainable(self):
        """Gets the is_explainable of this Feature.  # noqa: E501


        :return: The is_explainable of this Feature.  # noqa: E501
        :rtype: bool
        """
        return self._is_explainable

    @is_explainable.setter
    def is_explainable(self, is_explainable):
        """Sets the is_explainable of this Feature.


        :param is_explainable: The is_explainable of this Feature.  # noqa: E501
        :type: bool
        """
        if is_explainable is None:
            raise ValueError("Invalid value for `is_explainable`, must not be `None`")  # noqa: E501

        self._is_explainable = is_explainable

    @property
    def is_categorical(self):
        """Gets the is_categorical of this Feature.  # noqa: E501


        :return: The is_categorical of this Feature.  # noqa: E501
        :rtype: bool
        """
        return self._is_categorical

    @is_categorical.setter
    def is_categorical(self, is_categorical):
        """Sets the is_categorical of this Feature.


        :param is_categorical: The is_categorical of this Feature.  # noqa: E501
        :type: bool
        """
        if is_categorical is None:
            raise ValueError("Invalid value for `is_categorical`, must not be `None`")  # noqa: E501

        self._is_categorical = is_categorical

    @property
    def category_values(self):
        """Gets the category_values of this Feature.  # noqa: E501


        :return: The category_values of this Feature.  # noqa: E501
        :rtype: object
        """
        return self._category_values

    @category_values.setter
    def category_values(self, category_values):
        """Sets the category_values of this Feature.


        :param category_values: The category_values of this Feature.  # noqa: E501
        :type: object
        """

        self._category_values = category_values

    @property
    def type(self):
        """Gets the type of this Feature.  # noqa: E501


        :return: The type of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Feature.


        :param type: The type of this Feature.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def feature_table_id(self):
        """Gets the feature_table_id of this Feature.  # noqa: E501


        :return: The feature_table_id of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._feature_table_id

    @feature_table_id.setter
    def feature_table_id(self, feature_table_id):
        """Sets the feature_table_id of this Feature.


        :param feature_table_id: The feature_table_id of this Feature.  # noqa: E501
        :type: str
        """
        if feature_table_id is None:
            raise ValueError("Invalid value for `feature_table_id`, must not be `None`")  # noqa: E501

        self._feature_table_id = feature_table_id

    @property
    def feature_table(self):
        """Gets the feature_table of this Feature.  # noqa: E501


        :return: The feature_table of this Feature.  # noqa: E501
        :rtype: FeatureTable
        """
        return self._feature_table

    @feature_table.setter
    def feature_table(self, feature_table):
        """Sets the feature_table of this Feature.


        :param feature_table: The feature_table of this Feature.  # noqa: E501
        :type: FeatureTable
        """

        self._feature_table = feature_table

    @property
    def feature_sub_category(self):
        """Gets the feature_sub_category of this Feature.  # noqa: E501


        :return: The feature_sub_category of this Feature.  # noqa: E501
        :rtype: FeatureSubCategory
        """
        return self._feature_sub_category

    @feature_sub_category.setter
    def feature_sub_category(self, feature_sub_category):
        """Sets the feature_sub_category of this Feature.


        :param feature_sub_category: The feature_sub_category of this Feature.  # noqa: E501
        :type: FeatureSubCategory
        """

        self._feature_sub_category = feature_sub_category

    @property
    def model_job_output_features(self):
        """Gets the model_job_output_features of this Feature.  # noqa: E501


        :return: The model_job_output_features of this Feature.  # noqa: E501
        :rtype: list[ModelJobOutputFeature]
        """
        return self._model_job_output_features

    @model_job_output_features.setter
    def model_job_output_features(self, model_job_output_features):
        """Sets the model_job_output_features of this Feature.


        :param model_job_output_features: The model_job_output_features of this Feature.  # noqa: E501
        :type: list[ModelJobOutputFeature]
        """

        self._model_job_output_features = model_job_output_features

    @property
    def organization_feature_exclusions(self):
        """Gets the organization_feature_exclusions of this Feature.  # noqa: E501


        :return: The organization_feature_exclusions of this Feature.  # noqa: E501
        :rtype: list[OrganizationFeatureExclusion]
        """
        return self._organization_feature_exclusions

    @organization_feature_exclusions.setter
    def organization_feature_exclusions(self, organization_feature_exclusions):
        """Sets the organization_feature_exclusions of this Feature.


        :param organization_feature_exclusions: The organization_feature_exclusions of this Feature.  # noqa: E501
        :type: list[OrganizationFeatureExclusion]
        """

        self._organization_feature_exclusions = organization_feature_exclusions

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Feature.  # noqa: E501


        :return: The last_updated_by of this Feature.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Feature.


        :param last_updated_by: The last_updated_by of this Feature.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_at(self):
        """Gets the created_at of this Feature.  # noqa: E501


        :return: The created_at of this Feature.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Feature.


        :param created_at: The created_at of this Feature.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Feature.  # noqa: E501


        :return: The updated_at of this Feature.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Feature.


        :param updated_at: The updated_at of this Feature.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Feature.  # noqa: E501


        :return: The version of this Feature.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Feature.


        :param version: The version of this Feature.  # noqa: E501
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
        if issubclass(Feature, dict):
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
        if not isinstance(other, Feature):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
