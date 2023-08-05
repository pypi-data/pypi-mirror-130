# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetAccountIdTokenResult',
    'AwaitableGetAccountIdTokenResult',
    'get_account_id_token',
    'get_account_id_token_output',
]

@pulumi.output_type
class GetAccountIdTokenResult:
    """
    A collection of values returned by getAccountIdToken.
    """
    def __init__(__self__, delegates=None, id=None, id_token=None, include_email=None, target_audience=None, target_service_account=None):
        if delegates and not isinstance(delegates, list):
            raise TypeError("Expected argument 'delegates' to be a list")
        pulumi.set(__self__, "delegates", delegates)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if id_token and not isinstance(id_token, str):
            raise TypeError("Expected argument 'id_token' to be a str")
        pulumi.set(__self__, "id_token", id_token)
        if include_email and not isinstance(include_email, bool):
            raise TypeError("Expected argument 'include_email' to be a bool")
        pulumi.set(__self__, "include_email", include_email)
        if target_audience and not isinstance(target_audience, str):
            raise TypeError("Expected argument 'target_audience' to be a str")
        pulumi.set(__self__, "target_audience", target_audience)
        if target_service_account and not isinstance(target_service_account, str):
            raise TypeError("Expected argument 'target_service_account' to be a str")
        pulumi.set(__self__, "target_service_account", target_service_account)

    @property
    @pulumi.getter
    def delegates(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "delegates")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="idToken")
    def id_token(self) -> str:
        """
        The `id_token` representing the new generated identity.
        """
        return pulumi.get(self, "id_token")

    @property
    @pulumi.getter(name="includeEmail")
    def include_email(self) -> Optional[bool]:
        return pulumi.get(self, "include_email")

    @property
    @pulumi.getter(name="targetAudience")
    def target_audience(self) -> str:
        return pulumi.get(self, "target_audience")

    @property
    @pulumi.getter(name="targetServiceAccount")
    def target_service_account(self) -> Optional[str]:
        return pulumi.get(self, "target_service_account")


class AwaitableGetAccountIdTokenResult(GetAccountIdTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountIdTokenResult(
            delegates=self.delegates,
            id=self.id,
            id_token=self.id_token,
            include_email=self.include_email,
            target_audience=self.target_audience,
            target_service_account=self.target_service_account)


def get_account_id_token(delegates: Optional[Sequence[str]] = None,
                         include_email: Optional[bool] = None,
                         target_audience: Optional[str] = None,
                         target_service_account: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountIdTokenResult:
    """
    This data source provides a Google OpenID Connect (`oidc`) `id_token`.  Tokens issued from this data source are typically used to call external services that accept OIDC tokens for authentication (e.g. [Google Cloud Run](https://cloud.google.com/run/docs/authenticating/service-to-service)).

    For more information see
    [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html#IDToken).

    ## Example Usage

    ### ServiceAccount JSON Credential File.
      `service_account.get_account_id_token` will use the configured provider credentials

    ### Service Account Impersonation.
      `service_account.get_account_access_token` will use background impersonated credentials provided by `service_account.get_account_access_token`.

      Note: to use the following, you must grant `target_service_account` the
      `roles/iam.serviceAccountTokenCreator` role on itself.


    :param Sequence[str] delegates: Delegate chain of approvals needed to perform full impersonation. Specify the fully qualified service account name.   Used only when using impersonation mode.
    :param bool include_email: Include the verified email in the claim. Used only when using impersonation mode.
    :param str target_audience: The audience claim for the `id_token`.
    :param str target_service_account: The email of the service account being impersonated.  Used only when using impersonation mode.
    """
    __args__ = dict()
    __args__['delegates'] = delegates
    __args__['includeEmail'] = include_email
    __args__['targetAudience'] = target_audience
    __args__['targetServiceAccount'] = target_service_account
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:serviceAccount/getAccountIdToken:getAccountIdToken', __args__, opts=opts, typ=GetAccountIdTokenResult).value

    return AwaitableGetAccountIdTokenResult(
        delegates=__ret__.delegates,
        id=__ret__.id,
        id_token=__ret__.id_token,
        include_email=__ret__.include_email,
        target_audience=__ret__.target_audience,
        target_service_account=__ret__.target_service_account)


@_utilities.lift_output_func(get_account_id_token)
def get_account_id_token_output(delegates: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                include_email: Optional[pulumi.Input[Optional[bool]]] = None,
                                target_audience: Optional[pulumi.Input[str]] = None,
                                target_service_account: Optional[pulumi.Input[Optional[str]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountIdTokenResult]:
    """
    This data source provides a Google OpenID Connect (`oidc`) `id_token`.  Tokens issued from this data source are typically used to call external services that accept OIDC tokens for authentication (e.g. [Google Cloud Run](https://cloud.google.com/run/docs/authenticating/service-to-service)).

    For more information see
    [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html#IDToken).

    ## Example Usage

    ### ServiceAccount JSON Credential File.
      `service_account.get_account_id_token` will use the configured provider credentials

    ### Service Account Impersonation.
      `service_account.get_account_access_token` will use background impersonated credentials provided by `service_account.get_account_access_token`.

      Note: to use the following, you must grant `target_service_account` the
      `roles/iam.serviceAccountTokenCreator` role on itself.


    :param Sequence[str] delegates: Delegate chain of approvals needed to perform full impersonation. Specify the fully qualified service account name.   Used only when using impersonation mode.
    :param bool include_email: Include the verified email in the claim. Used only when using impersonation mode.
    :param str target_audience: The audience claim for the `id_token`.
    :param str target_service_account: The email of the service account being impersonated.  Used only when using impersonation mode.
    """
    ...
