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

class DatasetJobStatus(object):
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
        'step_name': 'str',
        'message': 'str',
        'log_level': 'str',
        'metadata': 'object',
        'order': 'float',
        'dataset_job_id': 'str',
        'last_updated_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'step_name': 'stepName',
        'message': 'message',
        'log_level': 'logLevel',
        'metadata': 'metadata',
        'order': 'order',
        'dataset_job_id': 'datasetJobId',
        'last_updated_by': 'lastUpdatedBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, step_name=None, message=None, log_level=None, metadata=None, order=None, dataset_job_id=None, last_updated_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """DatasetJobStatus - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._step_name = None
        self._message = None
        self._log_level = None
        self._metadata = None
        self._order = None
        self._dataset_job_id = None
        self._last_updated_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.step_name = step_name
        self.message = message
        self.log_level = log_level
        if metadata is not None:
            self.metadata = metadata
        if order is not None:
            self.order = order
        self.dataset_job_id = dataset_job_id
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
        """Gets the id of this DatasetJobStatus.  # noqa: E501


        :return: The id of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DatasetJobStatus.


        :param id: The id of this DatasetJobStatus.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def step_name(self):
        """Gets the step_name of this DatasetJobStatus.  # noqa: E501


        :return: The step_name of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._step_name

    @step_name.setter
    def step_name(self, step_name):
        """Sets the step_name of this DatasetJobStatus.


        :param step_name: The step_name of this DatasetJobStatus.  # noqa: E501
        :type: str
        """
        if step_name is None:
            raise ValueError("Invalid value for `step_name`, must not be `None`")  # noqa: E501

        self._step_name = step_name

    @property
    def message(self):
        """Gets the message of this DatasetJobStatus.  # noqa: E501


        :return: The message of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this DatasetJobStatus.


        :param message: The message of this DatasetJobStatus.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def log_level(self):
        """Gets the log_level of this DatasetJobStatus.  # noqa: E501


        :return: The log_level of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        """Sets the log_level of this DatasetJobStatus.


        :param log_level: The log_level of this DatasetJobStatus.  # noqa: E501
        :type: str
        """
        if log_level is None:
            raise ValueError("Invalid value for `log_level`, must not be `None`")  # noqa: E501

        self._log_level = log_level

    @property
    def metadata(self):
        """Gets the metadata of this DatasetJobStatus.  # noqa: E501


        :return: The metadata of this DatasetJobStatus.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DatasetJobStatus.


        :param metadata: The metadata of this DatasetJobStatus.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def order(self):
        """Gets the order of this DatasetJobStatus.  # noqa: E501


        :return: The order of this DatasetJobStatus.  # noqa: E501
        :rtype: float
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this DatasetJobStatus.


        :param order: The order of this DatasetJobStatus.  # noqa: E501
        :type: float
        """

        self._order = order

    @property
    def dataset_job_id(self):
        """Gets the dataset_job_id of this DatasetJobStatus.  # noqa: E501


        :return: The dataset_job_id of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._dataset_job_id

    @dataset_job_id.setter
    def dataset_job_id(self, dataset_job_id):
        """Sets the dataset_job_id of this DatasetJobStatus.


        :param dataset_job_id: The dataset_job_id of this DatasetJobStatus.  # noqa: E501
        :type: str
        """
        if dataset_job_id is None:
            raise ValueError("Invalid value for `dataset_job_id`, must not be `None`")  # noqa: E501

        self._dataset_job_id = dataset_job_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this DatasetJobStatus.  # noqa: E501


        :return: The last_updated_by of this DatasetJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this DatasetJobStatus.


        :param last_updated_by: The last_updated_by of this DatasetJobStatus.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_at(self):
        """Gets the created_at of this DatasetJobStatus.  # noqa: E501


        :return: The created_at of this DatasetJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DatasetJobStatus.


        :param created_at: The created_at of this DatasetJobStatus.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this DatasetJobStatus.  # noqa: E501


        :return: The updated_at of this DatasetJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DatasetJobStatus.


        :param updated_at: The updated_at of this DatasetJobStatus.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this DatasetJobStatus.  # noqa: E501


        :return: The version of this DatasetJobStatus.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DatasetJobStatus.


        :param version: The version of this DatasetJobStatus.  # noqa: E501
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
        if issubclass(DatasetJobStatus, dict):
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
        if not isinstance(other, DatasetJobStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
