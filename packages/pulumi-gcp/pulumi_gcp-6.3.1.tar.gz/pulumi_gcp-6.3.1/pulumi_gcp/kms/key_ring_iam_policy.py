# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['KeyRingIAMPolicyArgs', 'KeyRingIAMPolicy']

@pulumi.input_type
class KeyRingIAMPolicyArgs:
    def __init__(__self__, *,
                 key_ring_id: pulumi.Input[str],
                 policy_data: pulumi.Input[str]):
        """
        The set of arguments for constructing a KeyRingIAMPolicy resource.
        :param pulumi.Input[str] key_ring_id: The key ring ID, in the form
               `{project_id}/{location_name}/{key_ring_name}` or
               `{location_name}/{key_ring_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.get_iam_policy` data source.
        """
        pulumi.set(__self__, "key_ring_id", key_ring_id)
        pulumi.set(__self__, "policy_data", policy_data)

    @property
    @pulumi.getter(name="keyRingId")
    def key_ring_id(self) -> pulumi.Input[str]:
        """
        The key ring ID, in the form
        `{project_id}/{location_name}/{key_ring_name}` or
        `{location_name}/{key_ring_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "key_ring_id")

    @key_ring_id.setter
    def key_ring_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_ring_id", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Input[str]:
        """
        The policy data generated by
        a `organizations.get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_data", value)


@pulumi.input_type
class _KeyRingIAMPolicyState:
    def __init__(__self__, *,
                 etag: Optional[pulumi.Input[str]] = None,
                 key_ring_id: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KeyRingIAMPolicy resources.
        :param pulumi.Input[str] etag: (Computed) The etag of the key ring's IAM policy.
        :param pulumi.Input[str] key_ring_id: The key ring ID, in the form
               `{project_id}/{location_name}/{key_ring_name}` or
               `{location_name}/{key_ring_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.get_iam_policy` data source.
        """
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if key_ring_id is not None:
            pulumi.set(__self__, "key_ring_id", key_ring_id)
        if policy_data is not None:
            pulumi.set(__self__, "policy_data", policy_data)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the key ring's IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="keyRingId")
    def key_ring_id(self) -> Optional[pulumi.Input[str]]:
        """
        The key ring ID, in the form
        `{project_id}/{location_name}/{key_ring_name}` or
        `{location_name}/{key_ring_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "key_ring_id")

    @key_ring_id.setter
    def key_ring_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_ring_id", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> Optional[pulumi.Input[str]]:
        """
        The policy data generated by
        a `organizations.get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_data", value)


class KeyRingIAMPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_ring_id: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for KMS key ring. Each of these resources serves a different use case:

        * `kms.KeyRingIAMPolicy`: Authoritative. Sets the IAM policy for the key ring and replaces any existing policy already attached.
        * `kms.KeyRingIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the key ring are preserved.
        * `kms.KeyRingIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the key ring are preserved.

        > **Note:** `kms.KeyRingIAMPolicy` **cannot** be used in conjunction with `kms.KeyRingIAMBinding` and `kms.KeyRingIAMMember` or they will fight over what your policy should be.

        > **Note:** `kms.KeyRingIAMBinding` resources **can be** used in conjunction with `kms.KeyRingIAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\_kms\_key\_ring\_iam\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        keyring = gcp.kms.KeyRing("keyring", location="global")
        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        key_ring = gcp.kms.KeyRingIAMPolicy("keyRing",
            key_ring_id=keyring.id,
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        keyring = gcp.kms.KeyRing("keyring", location="global")
        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
            ),
        )])
        key_ring = gcp.kms.KeyRingIAMPolicy("keyRing",
            key_ring_id=keyring.id,
            policy_data=admin.policy_data)
        ```

        ## google\_kms\_key\_ring\_iam\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMBinding("keyRing",
            key_ring_id="your-key-ring-id",
            members=["user:jane@example.com"],
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMBinding("keyRing",
            condition=gcp.kms.KeyRingIAMBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            key_ring_id="your-key-ring-id",
            members=["user:jane@example.com"],
            role="roles/editor")
        ```

        ## google\_kms\_key\_ring\_iam\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMMember("keyRing",
            key_ring_id="your-key-ring-id",
            member="user:jane@example.com",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMMember("keyRing",
            condition=gcp.kms.KeyRingIAMMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            key_ring_id="your-key-ring-id",
            member="user:jane@example.com",
            role="roles/editor")
        ```

        ## Import

        IAM member imports use space-delimited identifiers; the resource in question, the role, and the account.

        This member resource can be imported using the `key_ring_id`, role, and account e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam "your-project-id/location-name/key-ring-name roles/viewer user:foo@example.com"
        ```

         IAM binding imports use space-delimited identifiers; the resource in question and the role.

        This binding resource can be imported using the `key_ring_id` and role, e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam "your-project-id/location-name/key-ring-name roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question.

        This policy resource can be imported using the `key_ring_id`, e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam your-project-id/location-name/key-ring-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_ring_id: The key ring ID, in the form
               `{project_id}/{location_name}/{key_ring_name}` or
               `{location_name}/{key_ring_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.get_iam_policy` data source.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyRingIAMPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for KMS key ring. Each of these resources serves a different use case:

        * `kms.KeyRingIAMPolicy`: Authoritative. Sets the IAM policy for the key ring and replaces any existing policy already attached.
        * `kms.KeyRingIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the key ring are preserved.
        * `kms.KeyRingIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the key ring are preserved.

        > **Note:** `kms.KeyRingIAMPolicy` **cannot** be used in conjunction with `kms.KeyRingIAMBinding` and `kms.KeyRingIAMMember` or they will fight over what your policy should be.

        > **Note:** `kms.KeyRingIAMBinding` resources **can be** used in conjunction with `kms.KeyRingIAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\_kms\_key\_ring\_iam\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        keyring = gcp.kms.KeyRing("keyring", location="global")
        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        key_ring = gcp.kms.KeyRingIAMPolicy("keyRing",
            key_ring_id=keyring.id,
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        keyring = gcp.kms.KeyRing("keyring", location="global")
        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
            ),
        )])
        key_ring = gcp.kms.KeyRingIAMPolicy("keyRing",
            key_ring_id=keyring.id,
            policy_data=admin.policy_data)
        ```

        ## google\_kms\_key\_ring\_iam\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMBinding("keyRing",
            key_ring_id="your-key-ring-id",
            members=["user:jane@example.com"],
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMBinding("keyRing",
            condition=gcp.kms.KeyRingIAMBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            key_ring_id="your-key-ring-id",
            members=["user:jane@example.com"],
            role="roles/editor")
        ```

        ## google\_kms\_key\_ring\_iam\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMMember("keyRing",
            key_ring_id="your-key-ring-id",
            member="user:jane@example.com",
            role="roles/editor")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        key_ring = gcp.kms.KeyRingIAMMember("keyRing",
            condition=gcp.kms.KeyRingIAMMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\"2020-01-01T00:00:00Z\")",
                title="expires_after_2019_12_31",
            ),
            key_ring_id="your-key-ring-id",
            member="user:jane@example.com",
            role="roles/editor")
        ```

        ## Import

        IAM member imports use space-delimited identifiers; the resource in question, the role, and the account.

        This member resource can be imported using the `key_ring_id`, role, and account e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam "your-project-id/location-name/key-ring-name roles/viewer user:foo@example.com"
        ```

         IAM binding imports use space-delimited identifiers; the resource in question and the role.

        This binding resource can be imported using the `key_ring_id` and role, e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam "your-project-id/location-name/key-ring-name roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question.

        This policy resource can be imported using the `key_ring_id`, e.g.

        ```sh
         $ pulumi import gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy key_ring_iam your-project-id/location-name/key-ring-name
        ```

        :param str resource_name: The name of the resource.
        :param KeyRingIAMPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyRingIAMPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_ring_id: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyRingIAMPolicyArgs.__new__(KeyRingIAMPolicyArgs)

            if key_ring_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_ring_id'")
            __props__.__dict__["key_ring_id"] = key_ring_id
            if policy_data is None and not opts.urn:
                raise TypeError("Missing required property 'policy_data'")
            __props__.__dict__["policy_data"] = policy_data
            __props__.__dict__["etag"] = None
        super(KeyRingIAMPolicy, __self__).__init__(
            'gcp:kms/keyRingIAMPolicy:KeyRingIAMPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            etag: Optional[pulumi.Input[str]] = None,
            key_ring_id: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None) -> 'KeyRingIAMPolicy':
        """
        Get an existing KeyRingIAMPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the key ring's IAM policy.
        :param pulumi.Input[str] key_ring_id: The key ring ID, in the form
               `{project_id}/{location_name}/{key_ring_name}` or
               `{location_name}/{key_ring_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.get_iam_policy` data source.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KeyRingIAMPolicyState.__new__(_KeyRingIAMPolicyState)

        __props__.__dict__["etag"] = etag
        __props__.__dict__["key_ring_id"] = key_ring_id
        __props__.__dict__["policy_data"] = policy_data
        return KeyRingIAMPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the key ring's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="keyRingId")
    def key_ring_id(self) -> pulumi.Output[str]:
        """
        The key ring ID, in the form
        `{project_id}/{location_name}/{key_ring_name}` or
        `{location_name}/{key_ring_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        return pulumi.get(self, "key_ring_id")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Output[str]:
        """
        The policy data generated by
        a `organizations.get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

