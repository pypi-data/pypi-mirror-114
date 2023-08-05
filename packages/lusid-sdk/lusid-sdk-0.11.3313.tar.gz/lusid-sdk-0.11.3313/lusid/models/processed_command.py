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

class ProcessedCommand(object):
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
        'description': 'str',
        'path': 'str',
        'user_id': 'User',
        'processed_time': 'datetime'
    }

    attribute_map = {
        'description': 'description',
        'path': 'path',
        'user_id': 'userId',
        'processed_time': 'processedTime'
    }

    required_map = {
        'description': 'required',
        'path': 'optional',
        'user_id': 'required',
        'processed_time': 'required'
    }

    def __init__(self, description=None, path=None, user_id=None, processed_time=None):  # noqa: E501
        """
        ProcessedCommand - a model defined in OpenAPI

        :param description:  The description of the command issued. (required)
        :type description: str
        :param path:  The unique identifier for the command including the request id.
        :type path: str
        :param user_id:  (required)
        :type user_id: lusid.User
        :param processed_time:  The asAt datetime that the events published by the processing of this command were committed to LUSID. (required)
        :type processed_time: datetime

        """  # noqa: E501

        self._description = None
        self._path = None
        self._user_id = None
        self._processed_time = None
        self.discriminator = None

        self.description = description
        self.path = path
        self.user_id = user_id
        self.processed_time = processed_time

    @property
    def description(self):
        """Gets the description of this ProcessedCommand.  # noqa: E501

        The description of the command issued.  # noqa: E501

        :return: The description of this ProcessedCommand.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ProcessedCommand.

        The description of the command issued.  # noqa: E501

        :param description: The description of this ProcessedCommand.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def path(self):
        """Gets the path of this ProcessedCommand.  # noqa: E501

        The unique identifier for the command including the request id.  # noqa: E501

        :return: The path of this ProcessedCommand.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ProcessedCommand.

        The unique identifier for the command including the request id.  # noqa: E501

        :param path: The path of this ProcessedCommand.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def user_id(self):
        """Gets the user_id of this ProcessedCommand.  # noqa: E501


        :return: The user_id of this ProcessedCommand.  # noqa: E501
        :rtype: User
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ProcessedCommand.


        :param user_id: The user_id of this ProcessedCommand.  # noqa: E501
        :type: User
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def processed_time(self):
        """Gets the processed_time of this ProcessedCommand.  # noqa: E501

        The asAt datetime that the events published by the processing of this command were committed to LUSID.  # noqa: E501

        :return: The processed_time of this ProcessedCommand.  # noqa: E501
        :rtype: datetime
        """
        return self._processed_time

    @processed_time.setter
    def processed_time(self, processed_time):
        """Sets the processed_time of this ProcessedCommand.

        The asAt datetime that the events published by the processing of this command were committed to LUSID.  # noqa: E501

        :param processed_time: The processed_time of this ProcessedCommand.  # noqa: E501
        :type: datetime
        """
        if processed_time is None:
            raise ValueError("Invalid value for `processed_time`, must not be `None`")  # noqa: E501

        self._processed_time = processed_time

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
        if not isinstance(other, ProcessedCommand):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
