# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Host(object):
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
        'kind': 'str',
        'id': 'str',
        'href': 'str',
        'cluster_id': 'str',
        'infra_env_id': 'str',
        'status': 'str',
        'status_info': 'str',
        'validations_info': 'str',
        'logs_info': 'LogsState',
        'status_updated_at': 'datetime',
        'progress': 'HostProgressInfo',
        'stage_started_at': 'datetime',
        'stage_updated_at': 'datetime',
        'progress_stages': 'list[HostStage]',
        'connectivity': 'str',
        'api_vip_connectivity': 'str',
        'inventory': 'str',
        'free_addresses': 'str',
        'ntp_sources': 'str',
        'disks_info': 'str',
        'role': 'HostRole',
        'suggested_role': 'HostRole',
        'bootstrap': 'bool',
        'logs_collected_at': 'str',
        'logs_started_at': 'str',
        'installer_version': 'str',
        'installation_disk_path': 'str',
        'installation_disk_id': 'str',
        'updated_at': 'datetime',
        'created_at': 'datetime',
        'checked_in_at': 'datetime',
        'discovery_agent_version': 'str',
        'requested_hostname': 'str',
        'user_name': 'str',
        'deleted_at': 'object',
        'ignition_config_overrides': 'str',
        'installer_args': 'str',
        'machine_config_pool_name': 'str',
        'images_status': 'str',
        'domain_name_resolutions': 'str',
        'ignition_endpoint_token_set': 'bool'
    }

    attribute_map = {
        'kind': 'kind',
        'id': 'id',
        'href': 'href',
        'cluster_id': 'cluster_id',
        'infra_env_id': 'infra_env_id',
        'status': 'status',
        'status_info': 'status_info',
        'validations_info': 'validations_info',
        'logs_info': 'logs_info',
        'status_updated_at': 'status_updated_at',
        'progress': 'progress',
        'stage_started_at': 'stage_started_at',
        'stage_updated_at': 'stage_updated_at',
        'progress_stages': 'progress_stages',
        'connectivity': 'connectivity',
        'api_vip_connectivity': 'api_vip_connectivity',
        'inventory': 'inventory',
        'free_addresses': 'free_addresses',
        'ntp_sources': 'ntp_sources',
        'disks_info': 'disks_info',
        'role': 'role',
        'suggested_role': 'suggested_role',
        'bootstrap': 'bootstrap',
        'logs_collected_at': 'logs_collected_at',
        'logs_started_at': 'logs_started_at',
        'installer_version': 'installer_version',
        'installation_disk_path': 'installation_disk_path',
        'installation_disk_id': 'installation_disk_id',
        'updated_at': 'updated_at',
        'created_at': 'created_at',
        'checked_in_at': 'checked_in_at',
        'discovery_agent_version': 'discovery_agent_version',
        'requested_hostname': 'requested_hostname',
        'user_name': 'user_name',
        'deleted_at': 'deleted_at',
        'ignition_config_overrides': 'ignition_config_overrides',
        'installer_args': 'installer_args',
        'machine_config_pool_name': 'machine_config_pool_name',
        'images_status': 'images_status',
        'domain_name_resolutions': 'domain_name_resolutions',
        'ignition_endpoint_token_set': 'ignition_endpoint_token_set'
    }

    def __init__(self, kind=None, id=None, href=None, cluster_id=None, infra_env_id=None, status=None, status_info=None, validations_info=None, logs_info=None, status_updated_at=None, progress=None, stage_started_at=None, stage_updated_at=None, progress_stages=None, connectivity=None, api_vip_connectivity=None, inventory=None, free_addresses=None, ntp_sources=None, disks_info=None, role=None, suggested_role=None, bootstrap=None, logs_collected_at=None, logs_started_at=None, installer_version=None, installation_disk_path=None, installation_disk_id=None, updated_at=None, created_at=None, checked_in_at=None, discovery_agent_version=None, requested_hostname=None, user_name=None, deleted_at=None, ignition_config_overrides=None, installer_args=None, machine_config_pool_name=None, images_status=None, domain_name_resolutions=None, ignition_endpoint_token_set=None):  # noqa: E501
        """Host - a model defined in Swagger"""  # noqa: E501

        self._kind = None
        self._id = None
        self._href = None
        self._cluster_id = None
        self._infra_env_id = None
        self._status = None
        self._status_info = None
        self._validations_info = None
        self._logs_info = None
        self._status_updated_at = None
        self._progress = None
        self._stage_started_at = None
        self._stage_updated_at = None
        self._progress_stages = None
        self._connectivity = None
        self._api_vip_connectivity = None
        self._inventory = None
        self._free_addresses = None
        self._ntp_sources = None
        self._disks_info = None
        self._role = None
        self._suggested_role = None
        self._bootstrap = None
        self._logs_collected_at = None
        self._logs_started_at = None
        self._installer_version = None
        self._installation_disk_path = None
        self._installation_disk_id = None
        self._updated_at = None
        self._created_at = None
        self._checked_in_at = None
        self._discovery_agent_version = None
        self._requested_hostname = None
        self._user_name = None
        self._deleted_at = None
        self._ignition_config_overrides = None
        self._installer_args = None
        self._machine_config_pool_name = None
        self._images_status = None
        self._domain_name_resolutions = None
        self._ignition_endpoint_token_set = None
        self.discriminator = None

        self.kind = kind
        self.id = id
        self.href = href
        if cluster_id is not None:
            self.cluster_id = cluster_id
        if infra_env_id is not None:
            self.infra_env_id = infra_env_id
        self.status = status
        self.status_info = status_info
        if validations_info is not None:
            self.validations_info = validations_info
        if logs_info is not None:
            self.logs_info = logs_info
        if status_updated_at is not None:
            self.status_updated_at = status_updated_at
        if progress is not None:
            self.progress = progress
        if stage_started_at is not None:
            self.stage_started_at = stage_started_at
        if stage_updated_at is not None:
            self.stage_updated_at = stage_updated_at
        if progress_stages is not None:
            self.progress_stages = progress_stages
        if connectivity is not None:
            self.connectivity = connectivity
        if api_vip_connectivity is not None:
            self.api_vip_connectivity = api_vip_connectivity
        if inventory is not None:
            self.inventory = inventory
        if free_addresses is not None:
            self.free_addresses = free_addresses
        if ntp_sources is not None:
            self.ntp_sources = ntp_sources
        if disks_info is not None:
            self.disks_info = disks_info
        if role is not None:
            self.role = role
        if suggested_role is not None:
            self.suggested_role = suggested_role
        if bootstrap is not None:
            self.bootstrap = bootstrap
        if logs_collected_at is not None:
            self.logs_collected_at = logs_collected_at
        if logs_started_at is not None:
            self.logs_started_at = logs_started_at
        if installer_version is not None:
            self.installer_version = installer_version
        if installation_disk_path is not None:
            self.installation_disk_path = installation_disk_path
        if installation_disk_id is not None:
            self.installation_disk_id = installation_disk_id
        if updated_at is not None:
            self.updated_at = updated_at
        if created_at is not None:
            self.created_at = created_at
        if checked_in_at is not None:
            self.checked_in_at = checked_in_at
        if discovery_agent_version is not None:
            self.discovery_agent_version = discovery_agent_version
        if requested_hostname is not None:
            self.requested_hostname = requested_hostname
        if user_name is not None:
            self.user_name = user_name
        if deleted_at is not None:
            self.deleted_at = deleted_at
        if ignition_config_overrides is not None:
            self.ignition_config_overrides = ignition_config_overrides
        if installer_args is not None:
            self.installer_args = installer_args
        if machine_config_pool_name is not None:
            self.machine_config_pool_name = machine_config_pool_name
        if images_status is not None:
            self.images_status = images_status
        if domain_name_resolutions is not None:
            self.domain_name_resolutions = domain_name_resolutions
        if ignition_endpoint_token_set is not None:
            self.ignition_endpoint_token_set = ignition_endpoint_token_set

    @property
    def kind(self):
        """Gets the kind of this Host.  # noqa: E501

        Indicates the type of this object. Will be 'Host' if this is a complete object or 'HostLink' if it is just a link, or 'AddToExistingClusterHost' for host being added to existing OCP cluster, or   # noqa: E501

        :return: The kind of this Host.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this Host.

        Indicates the type of this object. Will be 'Host' if this is a complete object or 'HostLink' if it is just a link, or 'AddToExistingClusterHost' for host being added to existing OCP cluster, or   # noqa: E501

        :param kind: The kind of this Host.  # noqa: E501
        :type: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501
        allowed_values = ["Host", "AddToExistingClusterHost"]  # noqa: E501
        if kind not in allowed_values:
            raise ValueError(
                "Invalid value for `kind` ({0}), must be one of {1}"  # noqa: E501
                .format(kind, allowed_values)
            )

        self._kind = kind

    @property
    def id(self):
        """Gets the id of this Host.  # noqa: E501

        Unique identifier of the object.  # noqa: E501

        :return: The id of this Host.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Host.

        Unique identifier of the object.  # noqa: E501

        :param id: The id of this Host.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def href(self):
        """Gets the href of this Host.  # noqa: E501

        Self link.  # noqa: E501

        :return: The href of this Host.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this Host.

        Self link.  # noqa: E501

        :param href: The href of this Host.  # noqa: E501
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")  # noqa: E501

        self._href = href

    @property
    def cluster_id(self):
        """Gets the cluster_id of this Host.  # noqa: E501

        The cluster that this host is associated with.  # noqa: E501

        :return: The cluster_id of this Host.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this Host.

        The cluster that this host is associated with.  # noqa: E501

        :param cluster_id: The cluster_id of this Host.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def infra_env_id(self):
        """Gets the infra_env_id of this Host.  # noqa: E501

        The infra-env that this host is associated with.  # noqa: E501

        :return: The infra_env_id of this Host.  # noqa: E501
        :rtype: str
        """
        return self._infra_env_id

    @infra_env_id.setter
    def infra_env_id(self, infra_env_id):
        """Sets the infra_env_id of this Host.

        The infra-env that this host is associated with.  # noqa: E501

        :param infra_env_id: The infra_env_id of this Host.  # noqa: E501
        :type: str
        """

        self._infra_env_id = infra_env_id

    @property
    def status(self):
        """Gets the status of this Host.  # noqa: E501


        :return: The status of this Host.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Host.


        :param status: The status of this Host.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["discovering", "known", "disconnected", "insufficient", "disabled", "preparing-for-installation", "preparing-failed", "preparing-successful", "pending-for-input", "installing", "installing-in-progress", "installing-pending-user-action", "resetting-pending-user-action", "installed", "error", "resetting", "added-to-existing-cluster", "cancelled", "binding", "unbinding", "unbinding-pending-user-action", "known-unbound", "disconnected-unbound", "insufficient-unbound", "disabled-unbound", "discovering-unbound"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def status_info(self):
        """Gets the status_info of this Host.  # noqa: E501


        :return: The status_info of this Host.  # noqa: E501
        :rtype: str
        """
        return self._status_info

    @status_info.setter
    def status_info(self, status_info):
        """Sets the status_info of this Host.


        :param status_info: The status_info of this Host.  # noqa: E501
        :type: str
        """
        if status_info is None:
            raise ValueError("Invalid value for `status_info`, must not be `None`")  # noqa: E501

        self._status_info = status_info

    @property
    def validations_info(self):
        """Gets the validations_info of this Host.  # noqa: E501

        JSON-formatted string containing the validation results for each validation id grouped by category (network, hardware, etc.)  # noqa: E501

        :return: The validations_info of this Host.  # noqa: E501
        :rtype: str
        """
        return self._validations_info

    @validations_info.setter
    def validations_info(self, validations_info):
        """Sets the validations_info of this Host.

        JSON-formatted string containing the validation results for each validation id grouped by category (network, hardware, etc.)  # noqa: E501

        :param validations_info: The validations_info of this Host.  # noqa: E501
        :type: str
        """

        self._validations_info = validations_info

    @property
    def logs_info(self):
        """Gets the logs_info of this Host.  # noqa: E501

        The progress of log collection or empty if logs are not applicable  # noqa: E501

        :return: The logs_info of this Host.  # noqa: E501
        :rtype: LogsState
        """
        return self._logs_info

    @logs_info.setter
    def logs_info(self, logs_info):
        """Sets the logs_info of this Host.

        The progress of log collection or empty if logs are not applicable  # noqa: E501

        :param logs_info: The logs_info of this Host.  # noqa: E501
        :type: LogsState
        """

        self._logs_info = logs_info

    @property
    def status_updated_at(self):
        """Gets the status_updated_at of this Host.  # noqa: E501

        The last time that the host status was updated.  # noqa: E501

        :return: The status_updated_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._status_updated_at

    @status_updated_at.setter
    def status_updated_at(self, status_updated_at):
        """Sets the status_updated_at of this Host.

        The last time that the host status was updated.  # noqa: E501

        :param status_updated_at: The status_updated_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._status_updated_at = status_updated_at

    @property
    def progress(self):
        """Gets the progress of this Host.  # noqa: E501


        :return: The progress of this Host.  # noqa: E501
        :rtype: HostProgressInfo
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this Host.


        :param progress: The progress of this Host.  # noqa: E501
        :type: HostProgressInfo
        """

        self._progress = progress

    @property
    def stage_started_at(self):
        """Gets the stage_started_at of this Host.  # noqa: E501

        Time at which the current progress stage started.  # noqa: E501

        :return: The stage_started_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._stage_started_at

    @stage_started_at.setter
    def stage_started_at(self, stage_started_at):
        """Sets the stage_started_at of this Host.

        Time at which the current progress stage started.  # noqa: E501

        :param stage_started_at: The stage_started_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._stage_started_at = stage_started_at

    @property
    def stage_updated_at(self):
        """Gets the stage_updated_at of this Host.  # noqa: E501

        Time at which the current progress stage was last updated.  # noqa: E501

        :return: The stage_updated_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._stage_updated_at

    @stage_updated_at.setter
    def stage_updated_at(self, stage_updated_at):
        """Sets the stage_updated_at of this Host.

        Time at which the current progress stage was last updated.  # noqa: E501

        :param stage_updated_at: The stage_updated_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._stage_updated_at = stage_updated_at

    @property
    def progress_stages(self):
        """Gets the progress_stages of this Host.  # noqa: E501


        :return: The progress_stages of this Host.  # noqa: E501
        :rtype: list[HostStage]
        """
        return self._progress_stages

    @progress_stages.setter
    def progress_stages(self, progress_stages):
        """Sets the progress_stages of this Host.


        :param progress_stages: The progress_stages of this Host.  # noqa: E501
        :type: list[HostStage]
        """

        self._progress_stages = progress_stages

    @property
    def connectivity(self):
        """Gets the connectivity of this Host.  # noqa: E501


        :return: The connectivity of this Host.  # noqa: E501
        :rtype: str
        """
        return self._connectivity

    @connectivity.setter
    def connectivity(self, connectivity):
        """Sets the connectivity of this Host.


        :param connectivity: The connectivity of this Host.  # noqa: E501
        :type: str
        """

        self._connectivity = connectivity

    @property
    def api_vip_connectivity(self):
        """Gets the api_vip_connectivity of this Host.  # noqa: E501


        :return: The api_vip_connectivity of this Host.  # noqa: E501
        :rtype: str
        """
        return self._api_vip_connectivity

    @api_vip_connectivity.setter
    def api_vip_connectivity(self, api_vip_connectivity):
        """Sets the api_vip_connectivity of this Host.


        :param api_vip_connectivity: The api_vip_connectivity of this Host.  # noqa: E501
        :type: str
        """

        self._api_vip_connectivity = api_vip_connectivity

    @property
    def inventory(self):
        """Gets the inventory of this Host.  # noqa: E501


        :return: The inventory of this Host.  # noqa: E501
        :rtype: str
        """
        return self._inventory

    @inventory.setter
    def inventory(self, inventory):
        """Sets the inventory of this Host.


        :param inventory: The inventory of this Host.  # noqa: E501
        :type: str
        """

        self._inventory = inventory

    @property
    def free_addresses(self):
        """Gets the free_addresses of this Host.  # noqa: E501


        :return: The free_addresses of this Host.  # noqa: E501
        :rtype: str
        """
        return self._free_addresses

    @free_addresses.setter
    def free_addresses(self, free_addresses):
        """Sets the free_addresses of this Host.


        :param free_addresses: The free_addresses of this Host.  # noqa: E501
        :type: str
        """

        self._free_addresses = free_addresses

    @property
    def ntp_sources(self):
        """Gets the ntp_sources of this Host.  # noqa: E501

        The configured NTP sources on the host.  # noqa: E501

        :return: The ntp_sources of this Host.  # noqa: E501
        :rtype: str
        """
        return self._ntp_sources

    @ntp_sources.setter
    def ntp_sources(self, ntp_sources):
        """Sets the ntp_sources of this Host.

        The configured NTP sources on the host.  # noqa: E501

        :param ntp_sources: The ntp_sources of this Host.  # noqa: E501
        :type: str
        """

        self._ntp_sources = ntp_sources

    @property
    def disks_info(self):
        """Gets the disks_info of this Host.  # noqa: E501

        Additional information about disks, formatted as JSON.  # noqa: E501

        :return: The disks_info of this Host.  # noqa: E501
        :rtype: str
        """
        return self._disks_info

    @disks_info.setter
    def disks_info(self, disks_info):
        """Sets the disks_info of this Host.

        Additional information about disks, formatted as JSON.  # noqa: E501

        :param disks_info: The disks_info of this Host.  # noqa: E501
        :type: str
        """

        self._disks_info = disks_info

    @property
    def role(self):
        """Gets the role of this Host.  # noqa: E501


        :return: The role of this Host.  # noqa: E501
        :rtype: HostRole
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this Host.


        :param role: The role of this Host.  # noqa: E501
        :type: HostRole
        """

        self._role = role

    @property
    def suggested_role(self):
        """Gets the suggested_role of this Host.  # noqa: E501


        :return: The suggested_role of this Host.  # noqa: E501
        :rtype: HostRole
        """
        return self._suggested_role

    @suggested_role.setter
    def suggested_role(self, suggested_role):
        """Sets the suggested_role of this Host.


        :param suggested_role: The suggested_role of this Host.  # noqa: E501
        :type: HostRole
        """

        self._suggested_role = suggested_role

    @property
    def bootstrap(self):
        """Gets the bootstrap of this Host.  # noqa: E501


        :return: The bootstrap of this Host.  # noqa: E501
        :rtype: bool
        """
        return self._bootstrap

    @bootstrap.setter
    def bootstrap(self, bootstrap):
        """Sets the bootstrap of this Host.


        :param bootstrap: The bootstrap of this Host.  # noqa: E501
        :type: bool
        """

        self._bootstrap = bootstrap

    @property
    def logs_collected_at(self):
        """Gets the logs_collected_at of this Host.  # noqa: E501


        :return: The logs_collected_at of this Host.  # noqa: E501
        :rtype: str
        """
        return self._logs_collected_at

    @logs_collected_at.setter
    def logs_collected_at(self, logs_collected_at):
        """Sets the logs_collected_at of this Host.


        :param logs_collected_at: The logs_collected_at of this Host.  # noqa: E501
        :type: str
        """

        self._logs_collected_at = logs_collected_at

    @property
    def logs_started_at(self):
        """Gets the logs_started_at of this Host.  # noqa: E501


        :return: The logs_started_at of this Host.  # noqa: E501
        :rtype: str
        """
        return self._logs_started_at

    @logs_started_at.setter
    def logs_started_at(self, logs_started_at):
        """Sets the logs_started_at of this Host.


        :param logs_started_at: The logs_started_at of this Host.  # noqa: E501
        :type: str
        """

        self._logs_started_at = logs_started_at

    @property
    def installer_version(self):
        """Gets the installer_version of this Host.  # noqa: E501

        Installer version.  # noqa: E501

        :return: The installer_version of this Host.  # noqa: E501
        :rtype: str
        """
        return self._installer_version

    @installer_version.setter
    def installer_version(self, installer_version):
        """Sets the installer_version of this Host.

        Installer version.  # noqa: E501

        :param installer_version: The installer_version of this Host.  # noqa: E501
        :type: str
        """

        self._installer_version = installer_version

    @property
    def installation_disk_path(self):
        """Gets the installation_disk_path of this Host.  # noqa: E501

        Contains the inventory disk path, This field is replaced by installation_disk_id field and used for backward compatability with the old UI.  # noqa: E501

        :return: The installation_disk_path of this Host.  # noqa: E501
        :rtype: str
        """
        return self._installation_disk_path

    @installation_disk_path.setter
    def installation_disk_path(self, installation_disk_path):
        """Sets the installation_disk_path of this Host.

        Contains the inventory disk path, This field is replaced by installation_disk_id field and used for backward compatability with the old UI.  # noqa: E501

        :param installation_disk_path: The installation_disk_path of this Host.  # noqa: E501
        :type: str
        """

        self._installation_disk_path = installation_disk_path

    @property
    def installation_disk_id(self):
        """Gets the installation_disk_id of this Host.  # noqa: E501

        Contains the inventory disk id to install on.  # noqa: E501

        :return: The installation_disk_id of this Host.  # noqa: E501
        :rtype: str
        """
        return self._installation_disk_id

    @installation_disk_id.setter
    def installation_disk_id(self, installation_disk_id):
        """Sets the installation_disk_id of this Host.

        Contains the inventory disk id to install on.  # noqa: E501

        :param installation_disk_id: The installation_disk_id of this Host.  # noqa: E501
        :type: str
        """

        self._installation_disk_id = installation_disk_id

    @property
    def updated_at(self):
        """Gets the updated_at of this Host.  # noqa: E501


        :return: The updated_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Host.


        :param updated_at: The updated_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def created_at(self):
        """Gets the created_at of this Host.  # noqa: E501


        :return: The created_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Host.


        :param created_at: The created_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def checked_in_at(self):
        """Gets the checked_in_at of this Host.  # noqa: E501

        The last time the host's agent communicated with the service.  # noqa: E501

        :return: The checked_in_at of this Host.  # noqa: E501
        :rtype: datetime
        """
        return self._checked_in_at

    @checked_in_at.setter
    def checked_in_at(self, checked_in_at):
        """Sets the checked_in_at of this Host.

        The last time the host's agent communicated with the service.  # noqa: E501

        :param checked_in_at: The checked_in_at of this Host.  # noqa: E501
        :type: datetime
        """

        self._checked_in_at = checked_in_at

    @property
    def discovery_agent_version(self):
        """Gets the discovery_agent_version of this Host.  # noqa: E501


        :return: The discovery_agent_version of this Host.  # noqa: E501
        :rtype: str
        """
        return self._discovery_agent_version

    @discovery_agent_version.setter
    def discovery_agent_version(self, discovery_agent_version):
        """Sets the discovery_agent_version of this Host.


        :param discovery_agent_version: The discovery_agent_version of this Host.  # noqa: E501
        :type: str
        """

        self._discovery_agent_version = discovery_agent_version

    @property
    def requested_hostname(self):
        """Gets the requested_hostname of this Host.  # noqa: E501


        :return: The requested_hostname of this Host.  # noqa: E501
        :rtype: str
        """
        return self._requested_hostname

    @requested_hostname.setter
    def requested_hostname(self, requested_hostname):
        """Sets the requested_hostname of this Host.


        :param requested_hostname: The requested_hostname of this Host.  # noqa: E501
        :type: str
        """

        self._requested_hostname = requested_hostname

    @property
    def user_name(self):
        """Gets the user_name of this Host.  # noqa: E501


        :return: The user_name of this Host.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this Host.


        :param user_name: The user_name of this Host.  # noqa: E501
        :type: str
        """

        self._user_name = user_name

    @property
    def deleted_at(self):
        """Gets the deleted_at of this Host.  # noqa: E501

        swagger:ignore  # noqa: E501

        :return: The deleted_at of this Host.  # noqa: E501
        :rtype: object
        """
        return self._deleted_at

    @deleted_at.setter
    def deleted_at(self, deleted_at):
        """Sets the deleted_at of this Host.

        swagger:ignore  # noqa: E501

        :param deleted_at: The deleted_at of this Host.  # noqa: E501
        :type: object
        """

        self._deleted_at = deleted_at

    @property
    def ignition_config_overrides(self):
        """Gets the ignition_config_overrides of this Host.  # noqa: E501

        Json formatted string containing the user overrides for the host's pointer ignition  # noqa: E501

        :return: The ignition_config_overrides of this Host.  # noqa: E501
        :rtype: str
        """
        return self._ignition_config_overrides

    @ignition_config_overrides.setter
    def ignition_config_overrides(self, ignition_config_overrides):
        """Sets the ignition_config_overrides of this Host.

        Json formatted string containing the user overrides for the host's pointer ignition  # noqa: E501

        :param ignition_config_overrides: The ignition_config_overrides of this Host.  # noqa: E501
        :type: str
        """

        self._ignition_config_overrides = ignition_config_overrides

    @property
    def installer_args(self):
        """Gets the installer_args of this Host.  # noqa: E501


        :return: The installer_args of this Host.  # noqa: E501
        :rtype: str
        """
        return self._installer_args

    @installer_args.setter
    def installer_args(self, installer_args):
        """Sets the installer_args of this Host.


        :param installer_args: The installer_args of this Host.  # noqa: E501
        :type: str
        """

        self._installer_args = installer_args

    @property
    def machine_config_pool_name(self):
        """Gets the machine_config_pool_name of this Host.  # noqa: E501


        :return: The machine_config_pool_name of this Host.  # noqa: E501
        :rtype: str
        """
        return self._machine_config_pool_name

    @machine_config_pool_name.setter
    def machine_config_pool_name(self, machine_config_pool_name):
        """Sets the machine_config_pool_name of this Host.


        :param machine_config_pool_name: The machine_config_pool_name of this Host.  # noqa: E501
        :type: str
        """

        self._machine_config_pool_name = machine_config_pool_name

    @property
    def images_status(self):
        """Gets the images_status of this Host.  # noqa: E501

        Array of image statuses.  # noqa: E501

        :return: The images_status of this Host.  # noqa: E501
        :rtype: str
        """
        return self._images_status

    @images_status.setter
    def images_status(self, images_status):
        """Sets the images_status of this Host.

        Array of image statuses.  # noqa: E501

        :param images_status: The images_status of this Host.  # noqa: E501
        :type: str
        """

        self._images_status = images_status

    @property
    def domain_name_resolutions(self):
        """Gets the domain_name_resolutions of this Host.  # noqa: E501

        The domain name resolution result.  # noqa: E501

        :return: The domain_name_resolutions of this Host.  # noqa: E501
        :rtype: str
        """
        return self._domain_name_resolutions

    @domain_name_resolutions.setter
    def domain_name_resolutions(self, domain_name_resolutions):
        """Sets the domain_name_resolutions of this Host.

        The domain name resolution result.  # noqa: E501

        :param domain_name_resolutions: The domain_name_resolutions of this Host.  # noqa: E501
        :type: str
        """

        self._domain_name_resolutions = domain_name_resolutions

    @property
    def ignition_endpoint_token_set(self):
        """Gets the ignition_endpoint_token_set of this Host.  # noqa: E501

        True if the token to fetch the ignition from ignition_endpoint_url is set.  # noqa: E501

        :return: The ignition_endpoint_token_set of this Host.  # noqa: E501
        :rtype: bool
        """
        return self._ignition_endpoint_token_set

    @ignition_endpoint_token_set.setter
    def ignition_endpoint_token_set(self, ignition_endpoint_token_set):
        """Sets the ignition_endpoint_token_set of this Host.

        True if the token to fetch the ignition from ignition_endpoint_url is set.  # noqa: E501

        :param ignition_endpoint_token_set: The ignition_endpoint_token_set of this Host.  # noqa: E501
        :type: bool
        """

        self._ignition_endpoint_token_set = ignition_endpoint_token_set

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
        if issubclass(Host, dict):
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
        if not isinstance(other, Host):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
