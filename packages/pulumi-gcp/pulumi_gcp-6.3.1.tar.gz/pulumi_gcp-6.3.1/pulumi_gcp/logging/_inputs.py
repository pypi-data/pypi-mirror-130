# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'BillingAccountSinkBigqueryOptionsArgs',
    'BillingAccountSinkExclusionArgs',
    'FolderSinkBigqueryOptionsArgs',
    'FolderSinkExclusionArgs',
    'MetricBucketOptionsArgs',
    'MetricBucketOptionsExplicitBucketsArgs',
    'MetricBucketOptionsExponentialBucketsArgs',
    'MetricBucketOptionsLinearBucketsArgs',
    'MetricMetricDescriptorArgs',
    'MetricMetricDescriptorLabelArgs',
    'OrganizationSinkBigqueryOptionsArgs',
    'OrganizationSinkExclusionArgs',
    'ProjectSinkBigqueryOptionsArgs',
    'ProjectSinkExclusionArgs',
]

@pulumi.input_type
class BillingAccountSinkBigqueryOptionsArgs:
    def __init__(__self__, *,
                 use_partitioned_tables: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] use_partitioned_tables: Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
               By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
               tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
               has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        pulumi.set(__self__, "use_partitioned_tables", use_partitioned_tables)

    @property
    @pulumi.getter(name="usePartitionedTables")
    def use_partitioned_tables(self) -> pulumi.Input[bool]:
        """
        Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
        By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
        tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
        has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        return pulumi.get(self, "use_partitioned_tables")

    @use_partitioned_tables.setter
    def use_partitioned_tables(self, value: pulumi.Input[bool]):
        pulumi.set(self, "use_partitioned_tables", value)


@pulumi.input_type
class BillingAccountSinkExclusionArgs:
    def __init__(__self__, *,
                 filter: pulumi.Input[str],
                 name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] filter: An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
               write a filter.
        :param pulumi.Input[str] name: A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        :param pulumi.Input[str] description: A description of this exclusion.
        :param pulumi.Input[bool] disabled: If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        pulumi.set(__self__, "filter", filter)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input[str]:
        """
        An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
        write a filter.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this exclusion.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)


@pulumi.input_type
class FolderSinkBigqueryOptionsArgs:
    def __init__(__self__, *,
                 use_partitioned_tables: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] use_partitioned_tables: Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
               By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
               tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
               has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        pulumi.set(__self__, "use_partitioned_tables", use_partitioned_tables)

    @property
    @pulumi.getter(name="usePartitionedTables")
    def use_partitioned_tables(self) -> pulumi.Input[bool]:
        """
        Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
        By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
        tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
        has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        return pulumi.get(self, "use_partitioned_tables")

    @use_partitioned_tables.setter
    def use_partitioned_tables(self, value: pulumi.Input[bool]):
        pulumi.set(self, "use_partitioned_tables", value)


@pulumi.input_type
class FolderSinkExclusionArgs:
    def __init__(__self__, *,
                 filter: pulumi.Input[str],
                 name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] filter: An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
               write a filter.
        :param pulumi.Input[str] name: A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        :param pulumi.Input[str] description: A description of this exclusion.
        :param pulumi.Input[bool] disabled: If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        pulumi.set(__self__, "filter", filter)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input[str]:
        """
        An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
        write a filter.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this exclusion.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)


@pulumi.input_type
class MetricBucketOptionsArgs:
    def __init__(__self__, *,
                 explicit_buckets: Optional[pulumi.Input['MetricBucketOptionsExplicitBucketsArgs']] = None,
                 exponential_buckets: Optional[pulumi.Input['MetricBucketOptionsExponentialBucketsArgs']] = None,
                 linear_buckets: Optional[pulumi.Input['MetricBucketOptionsLinearBucketsArgs']] = None):
        """
        :param pulumi.Input['MetricBucketOptionsExplicitBucketsArgs'] explicit_buckets: Specifies a set of buckets with arbitrary widths.
               Structure is documented below.
        :param pulumi.Input['MetricBucketOptionsExponentialBucketsArgs'] exponential_buckets: Specifies an exponential sequence of buckets that have a width that is proportional to the value of
               the lower bound. Each bucket represents a constant relative uncertainty on a specific value in the bucket.
               Structure is documented below.
        :param pulumi.Input['MetricBucketOptionsLinearBucketsArgs'] linear_buckets: Specifies a linear sequence of buckets that all have the same width (except overflow and underflow).
               Each bucket represents a constant absolute uncertainty on the specific value in the bucket.
               Structure is documented below.
        """
        if explicit_buckets is not None:
            pulumi.set(__self__, "explicit_buckets", explicit_buckets)
        if exponential_buckets is not None:
            pulumi.set(__self__, "exponential_buckets", exponential_buckets)
        if linear_buckets is not None:
            pulumi.set(__self__, "linear_buckets", linear_buckets)

    @property
    @pulumi.getter(name="explicitBuckets")
    def explicit_buckets(self) -> Optional[pulumi.Input['MetricBucketOptionsExplicitBucketsArgs']]:
        """
        Specifies a set of buckets with arbitrary widths.
        Structure is documented below.
        """
        return pulumi.get(self, "explicit_buckets")

    @explicit_buckets.setter
    def explicit_buckets(self, value: Optional[pulumi.Input['MetricBucketOptionsExplicitBucketsArgs']]):
        pulumi.set(self, "explicit_buckets", value)

    @property
    @pulumi.getter(name="exponentialBuckets")
    def exponential_buckets(self) -> Optional[pulumi.Input['MetricBucketOptionsExponentialBucketsArgs']]:
        """
        Specifies an exponential sequence of buckets that have a width that is proportional to the value of
        the lower bound. Each bucket represents a constant relative uncertainty on a specific value in the bucket.
        Structure is documented below.
        """
        return pulumi.get(self, "exponential_buckets")

    @exponential_buckets.setter
    def exponential_buckets(self, value: Optional[pulumi.Input['MetricBucketOptionsExponentialBucketsArgs']]):
        pulumi.set(self, "exponential_buckets", value)

    @property
    @pulumi.getter(name="linearBuckets")
    def linear_buckets(self) -> Optional[pulumi.Input['MetricBucketOptionsLinearBucketsArgs']]:
        """
        Specifies a linear sequence of buckets that all have the same width (except overflow and underflow).
        Each bucket represents a constant absolute uncertainty on the specific value in the bucket.
        Structure is documented below.
        """
        return pulumi.get(self, "linear_buckets")

    @linear_buckets.setter
    def linear_buckets(self, value: Optional[pulumi.Input['MetricBucketOptionsLinearBucketsArgs']]):
        pulumi.set(self, "linear_buckets", value)


@pulumi.input_type
class MetricBucketOptionsExplicitBucketsArgs:
    def __init__(__self__, *,
                 bounds: pulumi.Input[Sequence[pulumi.Input[float]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[float]]] bounds: The values must be monotonically increasing.
        """
        pulumi.set(__self__, "bounds", bounds)

    @property
    @pulumi.getter
    def bounds(self) -> pulumi.Input[Sequence[pulumi.Input[float]]]:
        """
        The values must be monotonically increasing.
        """
        return pulumi.get(self, "bounds")

    @bounds.setter
    def bounds(self, value: pulumi.Input[Sequence[pulumi.Input[float]]]):
        pulumi.set(self, "bounds", value)


@pulumi.input_type
class MetricBucketOptionsExponentialBucketsArgs:
    def __init__(__self__, *,
                 growth_factor: Optional[pulumi.Input[float]] = None,
                 num_finite_buckets: Optional[pulumi.Input[int]] = None,
                 scale: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[float] growth_factor: Must be greater than 1.
        :param pulumi.Input[int] num_finite_buckets: Must be greater than 0.
        :param pulumi.Input[float] scale: Must be greater than 0.
        """
        if growth_factor is not None:
            pulumi.set(__self__, "growth_factor", growth_factor)
        if num_finite_buckets is not None:
            pulumi.set(__self__, "num_finite_buckets", num_finite_buckets)
        if scale is not None:
            pulumi.set(__self__, "scale", scale)

    @property
    @pulumi.getter(name="growthFactor")
    def growth_factor(self) -> Optional[pulumi.Input[float]]:
        """
        Must be greater than 1.
        """
        return pulumi.get(self, "growth_factor")

    @growth_factor.setter
    def growth_factor(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "growth_factor", value)

    @property
    @pulumi.getter(name="numFiniteBuckets")
    def num_finite_buckets(self) -> Optional[pulumi.Input[int]]:
        """
        Must be greater than 0.
        """
        return pulumi.get(self, "num_finite_buckets")

    @num_finite_buckets.setter
    def num_finite_buckets(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "num_finite_buckets", value)

    @property
    @pulumi.getter
    def scale(self) -> Optional[pulumi.Input[float]]:
        """
        Must be greater than 0.
        """
        return pulumi.get(self, "scale")

    @scale.setter
    def scale(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "scale", value)


@pulumi.input_type
class MetricBucketOptionsLinearBucketsArgs:
    def __init__(__self__, *,
                 num_finite_buckets: Optional[pulumi.Input[int]] = None,
                 offset: Optional[pulumi.Input[float]] = None,
                 width: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[int] num_finite_buckets: Must be greater than 0.
        :param pulumi.Input[float] offset: Lower bound of the first bucket.
        :param pulumi.Input[float] width: Must be greater than 0.
        """
        if num_finite_buckets is not None:
            pulumi.set(__self__, "num_finite_buckets", num_finite_buckets)
        if offset is not None:
            pulumi.set(__self__, "offset", offset)
        if width is not None:
            pulumi.set(__self__, "width", width)

    @property
    @pulumi.getter(name="numFiniteBuckets")
    def num_finite_buckets(self) -> Optional[pulumi.Input[int]]:
        """
        Must be greater than 0.
        """
        return pulumi.get(self, "num_finite_buckets")

    @num_finite_buckets.setter
    def num_finite_buckets(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "num_finite_buckets", value)

    @property
    @pulumi.getter
    def offset(self) -> Optional[pulumi.Input[float]]:
        """
        Lower bound of the first bucket.
        """
        return pulumi.get(self, "offset")

    @offset.setter
    def offset(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "offset", value)

    @property
    @pulumi.getter
    def width(self) -> Optional[pulumi.Input[float]]:
        """
        Must be greater than 0.
        """
        return pulumi.get(self, "width")

    @width.setter
    def width(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "width", value)


@pulumi.input_type
class MetricMetricDescriptorArgs:
    def __init__(__self__, *,
                 metric_kind: pulumi.Input[str],
                 value_type: pulumi.Input[str],
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input['MetricMetricDescriptorLabelArgs']]]] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] metric_kind: Whether the metric records instantaneous values, changes to a value, etc.
               Some combinations of metricKind and valueType might not be supported.
               For counter metrics, set this to DELTA.
               Possible values are `DELTA`, `GAUGE`, and `CUMULATIVE`.
        :param pulumi.Input[str] value_type: The type of data that can be assigned to the label.
               Default value is `STRING`.
               Possible values are `BOOL`, `INT64`, and `STRING`.
        :param pulumi.Input[str] display_name: A concise name for the metric, which can be displayed in user interfaces. Use sentence case
               without an ending period, for example "Request count". This field is optional but it is
               recommended to be set for any metrics associated with user-visible concepts, such as Quota.
        :param pulumi.Input[Sequence[pulumi.Input['MetricMetricDescriptorLabelArgs']]] labels: The set of labels that can be used to describe a specific instance of this metric type. For
               example, the appengine.googleapis.com/http/server/response_latencies metric type has a label
               for the HTTP response code, response_code, so you can look at latencies for successful responses
               or just for responses that failed.
               Structure is documented below.
        :param pulumi.Input[str] unit: The unit in which the metric value is reported. It is only applicable if the valueType is
               `INT64`, `DOUBLE`, or `DISTRIBUTION`. The supported units are a subset of
               [The Unified Code for Units of Measure](http://unitsofmeasure.org/ucum.html) standard
        """
        pulumi.set(__self__, "metric_kind", metric_kind)
        pulumi.set(__self__, "value_type", value_type)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="metricKind")
    def metric_kind(self) -> pulumi.Input[str]:
        """
        Whether the metric records instantaneous values, changes to a value, etc.
        Some combinations of metricKind and valueType might not be supported.
        For counter metrics, set this to DELTA.
        Possible values are `DELTA`, `GAUGE`, and `CUMULATIVE`.
        """
        return pulumi.get(self, "metric_kind")

    @metric_kind.setter
    def metric_kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric_kind", value)

    @property
    @pulumi.getter(name="valueType")
    def value_type(self) -> pulumi.Input[str]:
        """
        The type of data that can be assigned to the label.
        Default value is `STRING`.
        Possible values are `BOOL`, `INT64`, and `STRING`.
        """
        return pulumi.get(self, "value_type")

    @value_type.setter
    def value_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "value_type", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A concise name for the metric, which can be displayed in user interfaces. Use sentence case
        without an ending period, for example "Request count". This field is optional but it is
        recommended to be set for any metrics associated with user-visible concepts, such as Quota.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MetricMetricDescriptorLabelArgs']]]]:
        """
        The set of labels that can be used to describe a specific instance of this metric type. For
        example, the appengine.googleapis.com/http/server/response_latencies metric type has a label
        for the HTTP response code, response_code, so you can look at latencies for successful responses
        or just for responses that failed.
        Structure is documented below.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MetricMetricDescriptorLabelArgs']]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        The unit in which the metric value is reported. It is only applicable if the valueType is
        `INT64`, `DOUBLE`, or `DISTRIBUTION`. The supported units are a subset of
        [The Unified Code for Units of Measure](http://unitsofmeasure.org/ucum.html) standard
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


@pulumi.input_type
class MetricMetricDescriptorLabelArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 value_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] key: The label key.
        :param pulumi.Input[str] description: A description of this metric, which is used in documentation. The maximum length of the
               description is 8000 characters.
        :param pulumi.Input[str] value_type: The type of data that can be assigned to the label.
               Default value is `STRING`.
               Possible values are `BOOL`, `INT64`, and `STRING`.
        """
        pulumi.set(__self__, "key", key)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if value_type is not None:
            pulumi.set(__self__, "value_type", value_type)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The label key.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this metric, which is used in documentation. The maximum length of the
        description is 8000 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="valueType")
    def value_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of data that can be assigned to the label.
        Default value is `STRING`.
        Possible values are `BOOL`, `INT64`, and `STRING`.
        """
        return pulumi.get(self, "value_type")

    @value_type.setter
    def value_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value_type", value)


@pulumi.input_type
class OrganizationSinkBigqueryOptionsArgs:
    def __init__(__self__, *,
                 use_partitioned_tables: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] use_partitioned_tables: Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
               By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
               tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
               has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        pulumi.set(__self__, "use_partitioned_tables", use_partitioned_tables)

    @property
    @pulumi.getter(name="usePartitionedTables")
    def use_partitioned_tables(self) -> pulumi.Input[bool]:
        """
        Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
        By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
        tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
        has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        return pulumi.get(self, "use_partitioned_tables")

    @use_partitioned_tables.setter
    def use_partitioned_tables(self, value: pulumi.Input[bool]):
        pulumi.set(self, "use_partitioned_tables", value)


@pulumi.input_type
class OrganizationSinkExclusionArgs:
    def __init__(__self__, *,
                 filter: pulumi.Input[str],
                 name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] filter: An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
               write a filter.
        :param pulumi.Input[str] name: A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        :param pulumi.Input[str] description: A description of this exclusion.
        :param pulumi.Input[bool] disabled: If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        pulumi.set(__self__, "filter", filter)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input[str]:
        """
        An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
        write a filter.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this exclusion.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)


@pulumi.input_type
class ProjectSinkBigqueryOptionsArgs:
    def __init__(__self__, *,
                 use_partitioned_tables: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] use_partitioned_tables: Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
               By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
               tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
               has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        pulumi.set(__self__, "use_partitioned_tables", use_partitioned_tables)

    @property
    @pulumi.getter(name="usePartitionedTables")
    def use_partitioned_tables(self) -> pulumi.Input[bool]:
        """
        Whether to use [BigQuery's partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables).
        By default, Logging creates dated tables based on the log entries' timestamps, e.g. syslog_20170523. With partitioned
        tables the date suffix is no longer present and [special query syntax](https://cloud.google.com/bigquery/docs/querying-partitioned-tables)
        has to be used instead. In both cases, tables are sharded based on UTC timezone.
        """
        return pulumi.get(self, "use_partitioned_tables")

    @use_partitioned_tables.setter
    def use_partitioned_tables(self, value: pulumi.Input[bool]):
        pulumi.set(self, "use_partitioned_tables", value)


@pulumi.input_type
class ProjectSinkExclusionArgs:
    def __init__(__self__, *,
                 filter: pulumi.Input[str],
                 name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 disabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] filter: An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
               write a filter.
        :param pulumi.Input[str] name: A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        :param pulumi.Input[str] description: A description of this exclusion.
        :param pulumi.Input[bool] disabled: If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        pulumi.set(__self__, "filter", filter)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input[str]:
        """
        An advanced logs filter that matches the log entries to be excluded. By using the sample function, you can exclude less than 100% of the matching log entries. See [Advanced Log Filters](https://cloud.google.com/logging/docs/view/advanced_filters) for information on how to
        write a filter.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        A client-assigned identifier, such as `load-balancer-exclusion`. Identifiers are limited to 100 characters and can include only letters, digits, underscores, hyphens, and periods. First character has to be alphanumeric.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this exclusion.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to True, then this exclusion is disabled and it does not exclude any log entries.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)


