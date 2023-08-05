# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

import types

__config__ = pulumi.Config('gcp')


class _ExportableConfig(types.ModuleType):
    @property
    def access_approval_custom_endpoint(self) -> Optional[str]:
        return __config__.get('accessApprovalCustomEndpoint')

    @property
    def access_context_manager_custom_endpoint(self) -> Optional[str]:
        return __config__.get('accessContextManagerCustomEndpoint')

    @property
    def access_token(self) -> Optional[str]:
        return __config__.get('accessToken')

    @property
    def active_directory_custom_endpoint(self) -> Optional[str]:
        return __config__.get('activeDirectoryCustomEndpoint')

    @property
    def api_gateway_custom_endpoint(self) -> Optional[str]:
        return __config__.get('apiGatewayCustomEndpoint')

    @property
    def apigee_custom_endpoint(self) -> Optional[str]:
        return __config__.get('apigeeCustomEndpoint')

    @property
    def app_engine_custom_endpoint(self) -> Optional[str]:
        return __config__.get('appEngineCustomEndpoint')

    @property
    def artifact_registry_custom_endpoint(self) -> Optional[str]:
        return __config__.get('artifactRegistryCustomEndpoint')

    @property
    def assured_workloads_custom_endpoint(self) -> Optional[str]:
        return __config__.get('assuredWorkloadsCustomEndpoint')

    @property
    def batching(self) -> Optional[str]:
        return __config__.get('batching')

    @property
    def big_query_custom_endpoint(self) -> Optional[str]:
        return __config__.get('bigQueryCustomEndpoint')

    @property
    def bigquery_connection_custom_endpoint(self) -> Optional[str]:
        return __config__.get('bigqueryConnectionCustomEndpoint')

    @property
    def bigquery_data_transfer_custom_endpoint(self) -> Optional[str]:
        return __config__.get('bigqueryDataTransferCustomEndpoint')

    @property
    def bigquery_reservation_custom_endpoint(self) -> Optional[str]:
        return __config__.get('bigqueryReservationCustomEndpoint')

    @property
    def bigtable_custom_endpoint(self) -> Optional[str]:
        return __config__.get('bigtableCustomEndpoint')

    @property
    def billing_custom_endpoint(self) -> Optional[str]:
        return __config__.get('billingCustomEndpoint')

    @property
    def billing_project(self) -> Optional[str]:
        return __config__.get('billingProject')

    @property
    def binary_authorization_custom_endpoint(self) -> Optional[str]:
        return __config__.get('binaryAuthorizationCustomEndpoint')

    @property
    def cloud_asset_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudAssetCustomEndpoint')

    @property
    def cloud_billing_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudBillingCustomEndpoint')

    @property
    def cloud_build_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudBuildCustomEndpoint')

    @property
    def cloud_build_worker_pool_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudBuildWorkerPoolCustomEndpoint')

    @property
    def cloud_functions_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudFunctionsCustomEndpoint')

    @property
    def cloud_identity_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudIdentityCustomEndpoint')

    @property
    def cloud_iot_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudIotCustomEndpoint')

    @property
    def cloud_resource_manager_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudResourceManagerCustomEndpoint')

    @property
    def cloud_run_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudRunCustomEndpoint')

    @property
    def cloud_scheduler_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudSchedulerCustomEndpoint')

    @property
    def cloud_tasks_custom_endpoint(self) -> Optional[str]:
        return __config__.get('cloudTasksCustomEndpoint')

    @property
    def composer_custom_endpoint(self) -> Optional[str]:
        return __config__.get('composerCustomEndpoint')

    @property
    def compute_custom_endpoint(self) -> Optional[str]:
        return __config__.get('computeCustomEndpoint')

    @property
    def container_analysis_custom_endpoint(self) -> Optional[str]:
        return __config__.get('containerAnalysisCustomEndpoint')

    @property
    def container_custom_endpoint(self) -> Optional[str]:
        return __config__.get('containerCustomEndpoint')

    @property
    def credentials(self) -> Optional[str]:
        return __config__.get('credentials')

    @property
    def data_catalog_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataCatalogCustomEndpoint')

    @property
    def data_fusion_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataFusionCustomEndpoint')

    @property
    def data_loss_prevention_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataLossPreventionCustomEndpoint')

    @property
    def dataflow_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataflowCustomEndpoint')

    @property
    def dataproc_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataprocCustomEndpoint')

    @property
    def dataproc_metastore_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dataprocMetastoreCustomEndpoint')

    @property
    def datastore_custom_endpoint(self) -> Optional[str]:
        return __config__.get('datastoreCustomEndpoint')

    @property
    def deployment_manager_custom_endpoint(self) -> Optional[str]:
        return __config__.get('deploymentManagerCustomEndpoint')

    @property
    def dialogflow_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dialogflowCustomEndpoint')

    @property
    def dialogflow_cx_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dialogflowCxCustomEndpoint')

    @property
    def disable_google_partner_name(self) -> Optional[bool]:
        return __config__.get_bool('disableGooglePartnerName')

    @property
    def dns_custom_endpoint(self) -> Optional[str]:
        return __config__.get('dnsCustomEndpoint')

    @property
    def essential_contacts_custom_endpoint(self) -> Optional[str]:
        return __config__.get('essentialContactsCustomEndpoint')

    @property
    def eventarc_custom_endpoint(self) -> Optional[str]:
        return __config__.get('eventarcCustomEndpoint')

    @property
    def filestore_custom_endpoint(self) -> Optional[str]:
        return __config__.get('filestoreCustomEndpoint')

    @property
    def firebase_custom_endpoint(self) -> Optional[str]:
        return __config__.get('firebaseCustomEndpoint')

    @property
    def firestore_custom_endpoint(self) -> Optional[str]:
        return __config__.get('firestoreCustomEndpoint')

    @property
    def game_services_custom_endpoint(self) -> Optional[str]:
        return __config__.get('gameServicesCustomEndpoint')

    @property
    def gke_hub_custom_endpoint(self) -> Optional[str]:
        return __config__.get('gkeHubCustomEndpoint')

    @property
    def gkehub_feature_custom_endpoint(self) -> Optional[str]:
        return __config__.get('gkehubFeatureCustomEndpoint')

    @property
    def google_partner_name(self) -> Optional[str]:
        return __config__.get('googlePartnerName')

    @property
    def healthcare_custom_endpoint(self) -> Optional[str]:
        return __config__.get('healthcareCustomEndpoint')

    @property
    def iam_beta_custom_endpoint(self) -> Optional[str]:
        return __config__.get('iamBetaCustomEndpoint')

    @property
    def iam_credentials_custom_endpoint(self) -> Optional[str]:
        return __config__.get('iamCredentialsCustomEndpoint')

    @property
    def iam_custom_endpoint(self) -> Optional[str]:
        return __config__.get('iamCustomEndpoint')

    @property
    def iap_custom_endpoint(self) -> Optional[str]:
        return __config__.get('iapCustomEndpoint')

    @property
    def identity_platform_custom_endpoint(self) -> Optional[str]:
        return __config__.get('identityPlatformCustomEndpoint')

    @property
    def impersonate_service_account(self) -> Optional[str]:
        return __config__.get('impersonateServiceAccount')

    @property
    def impersonate_service_account_delegates(self) -> Optional[str]:
        return __config__.get('impersonateServiceAccountDelegates')

    @property
    def kms_custom_endpoint(self) -> Optional[str]:
        return __config__.get('kmsCustomEndpoint')

    @property
    def logging_custom_endpoint(self) -> Optional[str]:
        return __config__.get('loggingCustomEndpoint')

    @property
    def memcache_custom_endpoint(self) -> Optional[str]:
        return __config__.get('memcacheCustomEndpoint')

    @property
    def ml_engine_custom_endpoint(self) -> Optional[str]:
        return __config__.get('mlEngineCustomEndpoint')

    @property
    def monitoring_custom_endpoint(self) -> Optional[str]:
        return __config__.get('monitoringCustomEndpoint')

    @property
    def network_management_custom_endpoint(self) -> Optional[str]:
        return __config__.get('networkManagementCustomEndpoint')

    @property
    def network_services_custom_endpoint(self) -> Optional[str]:
        return __config__.get('networkServicesCustomEndpoint')

    @property
    def notebooks_custom_endpoint(self) -> Optional[str]:
        return __config__.get('notebooksCustomEndpoint')

    @property
    def org_policy_custom_endpoint(self) -> Optional[str]:
        return __config__.get('orgPolicyCustomEndpoint')

    @property
    def os_config_custom_endpoint(self) -> Optional[str]:
        return __config__.get('osConfigCustomEndpoint')

    @property
    def os_login_custom_endpoint(self) -> Optional[str]:
        return __config__.get('osLoginCustomEndpoint')

    @property
    def privateca_custom_endpoint(self) -> Optional[str]:
        return __config__.get('privatecaCustomEndpoint')

    @property
    def project(self) -> Optional[str]:
        return __config__.get('project') or _utilities.get_env('GOOGLE_PROJECT', 'GOOGLE_CLOUD_PROJECT', 'GCLOUD_PROJECT', 'CLOUDSDK_CORE_PROJECT')

    @property
    def pubsub_custom_endpoint(self) -> Optional[str]:
        return __config__.get('pubsubCustomEndpoint')

    @property
    def pubsub_lite_custom_endpoint(self) -> Optional[str]:
        return __config__.get('pubsubLiteCustomEndpoint')

    @property
    def redis_custom_endpoint(self) -> Optional[str]:
        return __config__.get('redisCustomEndpoint')

    @property
    def region(self) -> Optional[str]:
        return __config__.get('region') or _utilities.get_env('GOOGLE_REGION', 'GCLOUD_REGION', 'CLOUDSDK_COMPUTE_REGION')

    @property
    def request_reason(self) -> Optional[str]:
        return __config__.get('requestReason')

    @property
    def request_timeout(self) -> Optional[str]:
        return __config__.get('requestTimeout')

    @property
    def resource_manager_custom_endpoint(self) -> Optional[str]:
        return __config__.get('resourceManagerCustomEndpoint')

    @property
    def resource_manager_v2_custom_endpoint(self) -> Optional[str]:
        return __config__.get('resourceManagerV2CustomEndpoint')

    @property
    def runtime_config_custom_endpoint(self) -> Optional[str]:
        return __config__.get('runtimeConfigCustomEndpoint')

    @property
    def runtimeconfig_custom_endpoint(self) -> Optional[str]:
        return __config__.get('runtimeconfigCustomEndpoint')

    @property
    def scopes(self) -> Optional[str]:
        return __config__.get('scopes')

    @property
    def secret_manager_custom_endpoint(self) -> Optional[str]:
        return __config__.get('secretManagerCustomEndpoint')

    @property
    def security_center_custom_endpoint(self) -> Optional[str]:
        return __config__.get('securityCenterCustomEndpoint')

    @property
    def security_scanner_custom_endpoint(self) -> Optional[str]:
        return __config__.get('securityScannerCustomEndpoint')

    @property
    def service_directory_custom_endpoint(self) -> Optional[str]:
        return __config__.get('serviceDirectoryCustomEndpoint')

    @property
    def service_management_custom_endpoint(self) -> Optional[str]:
        return __config__.get('serviceManagementCustomEndpoint')

    @property
    def service_networking_custom_endpoint(self) -> Optional[str]:
        return __config__.get('serviceNetworkingCustomEndpoint')

    @property
    def service_usage_custom_endpoint(self) -> Optional[str]:
        return __config__.get('serviceUsageCustomEndpoint')

    @property
    def source_repo_custom_endpoint(self) -> Optional[str]:
        return __config__.get('sourceRepoCustomEndpoint')

    @property
    def spanner_custom_endpoint(self) -> Optional[str]:
        return __config__.get('spannerCustomEndpoint')

    @property
    def sql_custom_endpoint(self) -> Optional[str]:
        return __config__.get('sqlCustomEndpoint')

    @property
    def storage_custom_endpoint(self) -> Optional[str]:
        return __config__.get('storageCustomEndpoint')

    @property
    def storage_transfer_custom_endpoint(self) -> Optional[str]:
        return __config__.get('storageTransferCustomEndpoint')

    @property
    def tags_custom_endpoint(self) -> Optional[str]:
        return __config__.get('tagsCustomEndpoint')

    @property
    def tpu_custom_endpoint(self) -> Optional[str]:
        return __config__.get('tpuCustomEndpoint')

    @property
    def user_project_override(self) -> Optional[bool]:
        return __config__.get_bool('userProjectOverride')

    @property
    def vertex_ai_custom_endpoint(self) -> Optional[str]:
        return __config__.get('vertexAiCustomEndpoint')

    @property
    def vpc_access_custom_endpoint(self) -> Optional[str]:
        return __config__.get('vpcAccessCustomEndpoint')

    @property
    def workflows_custom_endpoint(self) -> Optional[str]:
        return __config__.get('workflowsCustomEndpoint')

    @property
    def zone(self) -> Optional[str]:
        return __config__.get('zone') or _utilities.get_env('GOOGLE_ZONE', 'GCLOUD_ZONE', 'CLOUDSDK_COMPUTE_ZONE')

