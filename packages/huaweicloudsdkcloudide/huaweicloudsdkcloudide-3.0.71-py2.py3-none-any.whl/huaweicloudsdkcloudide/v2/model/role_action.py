# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RoleAction:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'action_cname': 'str',
        'actions': 'str',
        'id': 'str',
        'role_id': 'str'
    }

    attribute_map = {
        'action_cname': 'action_cname',
        'actions': 'actions',
        'id': 'id',
        'role_id': 'role_id'
    }

    def __init__(self, action_cname=None, actions=None, id=None, role_id=None):
        """RoleAction - a model defined in huaweicloud sdk"""
        
        

        self._action_cname = None
        self._actions = None
        self._id = None
        self._role_id = None
        self.discriminator = None

        if action_cname is not None:
            self.action_cname = action_cname
        if actions is not None:
            self.actions = actions
        if id is not None:
            self.id = id
        if role_id is not None:
            self.role_id = role_id

    @property
    def action_cname(self):
        """Gets the action_cname of this RoleAction.

        动作名

        :return: The action_cname of this RoleAction.
        :rtype: str
        """
        return self._action_cname

    @action_cname.setter
    def action_cname(self, action_cname):
        """Sets the action_cname of this RoleAction.

        动作名

        :param action_cname: The action_cname of this RoleAction.
        :type: str
        """
        self._action_cname = action_cname

    @property
    def actions(self):
        """Gets the actions of this RoleAction.

        执行动作 。 - CREATE_INSTANCE 创建实例 - DELETE_INSTANCE 删除实例 - UPDATE_INSTANCE 修改实例 - QUERY_INSTANCE 查询实例列表 - RUN_INSTANCE 运行实例 - CREATE_SUB_ORG 创建子组织 - UPDATE_SUB_ORG 修改子组织 - DELETE_SUB_ORG 删除子组织 - QUERY_SUB_ORG 查询子组织列表 - ADD_USER_TO_ORG 新增组织中用户 - SET_USER_ROLES 设置用户角色 - DELETE_USER_IN_ORG 删除组织中用户 - QUERY_USER_IN_ORG 查询组织中用户列表

        :return: The actions of this RoleAction.
        :rtype: str
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this RoleAction.

        执行动作 。 - CREATE_INSTANCE 创建实例 - DELETE_INSTANCE 删除实例 - UPDATE_INSTANCE 修改实例 - QUERY_INSTANCE 查询实例列表 - RUN_INSTANCE 运行实例 - CREATE_SUB_ORG 创建子组织 - UPDATE_SUB_ORG 修改子组织 - DELETE_SUB_ORG 删除子组织 - QUERY_SUB_ORG 查询子组织列表 - ADD_USER_TO_ORG 新增组织中用户 - SET_USER_ROLES 设置用户角色 - DELETE_USER_IN_ORG 删除组织中用户 - QUERY_USER_IN_ORG 查询组织中用户列表

        :param actions: The actions of this RoleAction.
        :type: str
        """
        self._actions = actions

    @property
    def id(self):
        """Gets the id of this RoleAction.

        id

        :return: The id of this RoleAction.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RoleAction.

        id

        :param id: The id of this RoleAction.
        :type: str
        """
        self._id = id

    @property
    def role_id(self):
        """Gets the role_id of this RoleAction.

        角色id

        :return: The role_id of this RoleAction.
        :rtype: str
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        """Sets the role_id of this RoleAction.

        角色id

        :param role_id: The role_id of this RoleAction.
        :type: str
        """
        self._role_id = role_id

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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RoleAction):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
