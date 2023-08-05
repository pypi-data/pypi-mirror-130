# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'AccessApprovalSettingsEnrolledService',
    'IAMAuditConfigAuditLogConfig',
    'IAMBindingCondition',
    'IAMMemberCondition',
    'OrganizationPolicyBooleanPolicy',
    'OrganizationPolicyListPolicy',
    'OrganizationPolicyListPolicyAllow',
    'OrganizationPolicyListPolicyDeny',
    'OrganizationPolicyRestorePolicy',
    'GetOrganizationPolicyBooleanPolicyResult',
    'GetOrganizationPolicyListPolicyResult',
    'GetOrganizationPolicyListPolicyAllowResult',
    'GetOrganizationPolicyListPolicyDenyResult',
    'GetOrganizationPolicyRestorePolicyResult',
    'GetProjectProjectResult',
]

@pulumi.output_type
class AccessApprovalSettingsEnrolledService(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudProduct":
            suggest = "cloud_product"
        elif key == "enrollmentLevel":
            suggest = "enrollment_level"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessApprovalSettingsEnrolledService. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessApprovalSettingsEnrolledService.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessApprovalSettingsEnrolledService.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_product: str,
                 enrollment_level: Optional[str] = None):
        """
        :param str cloud_product: The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
               all
               appengine.googleapis.com
               bigquery.googleapis.com
               bigtable.googleapis.com
               cloudkms.googleapis.com
               compute.googleapis.com
               dataflow.googleapis.com
               iam.googleapis.com
               pubsub.googleapis.com
               storage.googleapis.com
        :param str enrollment_level: The enrollment level of the service.
               Default value is `BLOCK_ALL`.
               Possible values are `BLOCK_ALL`.
        """
        pulumi.set(__self__, "cloud_product", cloud_product)
        if enrollment_level is not None:
            pulumi.set(__self__, "enrollment_level", enrollment_level)

    @property
    @pulumi.getter(name="cloudProduct")
    def cloud_product(self) -> str:
        """
        The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
        all
        appengine.googleapis.com
        bigquery.googleapis.com
        bigtable.googleapis.com
        cloudkms.googleapis.com
        compute.googleapis.com
        dataflow.googleapis.com
        iam.googleapis.com
        pubsub.googleapis.com
        storage.googleapis.com
        """
        return pulumi.get(self, "cloud_product")

    @property
    @pulumi.getter(name="enrollmentLevel")
    def enrollment_level(self) -> Optional[str]:
        """
        The enrollment level of the service.
        Default value is `BLOCK_ALL`.
        Possible values are `BLOCK_ALL`.
        """
        return pulumi.get(self, "enrollment_level")


@pulumi.output_type
class IAMAuditConfigAuditLogConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logType":
            suggest = "log_type"
        elif key == "exemptedMembers":
            suggest = "exempted_members"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IAMAuditConfigAuditLogConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IAMAuditConfigAuditLogConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IAMAuditConfigAuditLogConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_type: str,
                 exempted_members: Optional[Sequence[str]] = None):
        """
        :param str log_type: Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        :param Sequence[str] exempted_members: Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
        """
        pulumi.set(__self__, "log_type", log_type)
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        """
        return pulumi.get(self, "log_type")

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[Sequence[str]]:
        """
        Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
        """
        return pulumi.get(self, "exempted_members")


@pulumi.output_type
class IAMBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str title: A title for the expression, i.e. a short string describing its purpose.
        :param str description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class IAMMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str title: A title for the expression, i.e. a short string describing its purpose.
        :param str description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class OrganizationPolicyBooleanPolicy(dict):
    def __init__(__self__, *,
                 enforced: bool):
        """
        :param bool enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        pulumi.set(__self__, "enforced", enforced)

    @property
    @pulumi.getter
    def enforced(self) -> bool:
        """
        If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        return pulumi.get(self, "enforced")


@pulumi.output_type
class OrganizationPolicyListPolicy(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "inheritFromParent":
            suggest = "inherit_from_parent"
        elif key == "suggestedValue":
            suggest = "suggested_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationPolicyListPolicy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationPolicyListPolicy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationPolicyListPolicy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allow: Optional['outputs.OrganizationPolicyListPolicyAllow'] = None,
                 deny: Optional['outputs.OrganizationPolicyListPolicyDeny'] = None,
                 inherit_from_parent: Optional[bool] = None,
                 suggested_value: Optional[str] = None):
        """
        :param 'OrganizationPolicyListPolicyAllowArgs' allow: or `deny` - (Optional) One or the other must be set.
        :param bool inherit_from_parent: If set to true, the values from the effective Policy of the parent resource
               are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        :param str suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        if allow is not None:
            pulumi.set(__self__, "allow", allow)
        if deny is not None:
            pulumi.set(__self__, "deny", deny)
        if inherit_from_parent is not None:
            pulumi.set(__self__, "inherit_from_parent", inherit_from_parent)
        if suggested_value is not None:
            pulumi.set(__self__, "suggested_value", suggested_value)

    @property
    @pulumi.getter
    def allow(self) -> Optional['outputs.OrganizationPolicyListPolicyAllow']:
        """
        or `deny` - (Optional) One or the other must be set.
        """
        return pulumi.get(self, "allow")

    @property
    @pulumi.getter
    def deny(self) -> Optional['outputs.OrganizationPolicyListPolicyDeny']:
        return pulumi.get(self, "deny")

    @property
    @pulumi.getter(name="inheritFromParent")
    def inherit_from_parent(self) -> Optional[bool]:
        """
        If set to true, the values from the effective Policy of the parent resource
        are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        """
        return pulumi.get(self, "inherit_from_parent")

    @property
    @pulumi.getter(name="suggestedValue")
    def suggested_value(self) -> Optional[str]:
        """
        The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        return pulumi.get(self, "suggested_value")


@pulumi.output_type
class OrganizationPolicyListPolicyAllow(dict):
    def __init__(__self__, *,
                 all: Optional[bool] = None,
                 values: Optional[Sequence[str]] = None):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[bool]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class OrganizationPolicyListPolicyDeny(dict):
    def __init__(__self__, *,
                 all: Optional[bool] = None,
                 values: Optional[Sequence[str]] = None):
        """
        :param bool all: The policy allows or denies all values.
        :param Sequence[str] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[bool]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class OrganizationPolicyRestorePolicy(dict):
    def __init__(__self__, *,
                 default: bool):
        """
        :param bool default: May only be set to true. If set, then the default Policy is restored.
        """
        pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def default(self) -> bool:
        """
        May only be set to true. If set, then the default Policy is restored.
        """
        return pulumi.get(self, "default")


@pulumi.output_type
class GetOrganizationPolicyBooleanPolicyResult(dict):
    def __init__(__self__, *,
                 enforced: bool):
        pulumi.set(__self__, "enforced", enforced)

    @property
    @pulumi.getter
    def enforced(self) -> bool:
        return pulumi.get(self, "enforced")


@pulumi.output_type
class GetOrganizationPolicyListPolicyResult(dict):
    def __init__(__self__, *,
                 allows: Sequence['outputs.GetOrganizationPolicyListPolicyAllowResult'],
                 denies: Sequence['outputs.GetOrganizationPolicyListPolicyDenyResult'],
                 inherit_from_parent: bool,
                 suggested_value: str):
        pulumi.set(__self__, "allows", allows)
        pulumi.set(__self__, "denies", denies)
        pulumi.set(__self__, "inherit_from_parent", inherit_from_parent)
        pulumi.set(__self__, "suggested_value", suggested_value)

    @property
    @pulumi.getter
    def allows(self) -> Sequence['outputs.GetOrganizationPolicyListPolicyAllowResult']:
        return pulumi.get(self, "allows")

    @property
    @pulumi.getter
    def denies(self) -> Sequence['outputs.GetOrganizationPolicyListPolicyDenyResult']:
        return pulumi.get(self, "denies")

    @property
    @pulumi.getter(name="inheritFromParent")
    def inherit_from_parent(self) -> bool:
        return pulumi.get(self, "inherit_from_parent")

    @property
    @pulumi.getter(name="suggestedValue")
    def suggested_value(self) -> str:
        return pulumi.get(self, "suggested_value")


@pulumi.output_type
class GetOrganizationPolicyListPolicyAllowResult(dict):
    def __init__(__self__, *,
                 all: bool,
                 values: Sequence[str]):
        pulumi.set(__self__, "all", all)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> bool:
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        return pulumi.get(self, "values")


@pulumi.output_type
class GetOrganizationPolicyListPolicyDenyResult(dict):
    def __init__(__self__, *,
                 all: bool,
                 values: Sequence[str]):
        pulumi.set(__self__, "all", all)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> bool:
        return pulumi.get(self, "all")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        return pulumi.get(self, "values")


@pulumi.output_type
class GetOrganizationPolicyRestorePolicyResult(dict):
    def __init__(__self__, *,
                 default: bool):
        pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def default(self) -> bool:
        return pulumi.get(self, "default")


@pulumi.output_type
class GetProjectProjectResult(dict):
    def __init__(__self__, *,
                 create_time: str,
                 labels: Mapping[str, str],
                 lifecycle_state: str,
                 name: str,
                 number: str,
                 parent: Mapping[str, str],
                 project_id: str):
        """
        :param str project_id: The project id of the project.
        """
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "labels", labels)
        pulumi.set(__self__, "lifecycle_state", lifecycle_state)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "number", number)
        pulumi.set(__self__, "parent", parent)
        pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="lifecycleState")
    def lifecycle_state(self) -> str:
        return pulumi.get(self, "lifecycle_state")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def number(self) -> str:
        return pulumi.get(self, "number")

    @property
    @pulumi.getter
    def parent(self) -> Mapping[str, str]:
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        """
        The project id of the project.
        """
        return pulumi.get(self, "project_id")


