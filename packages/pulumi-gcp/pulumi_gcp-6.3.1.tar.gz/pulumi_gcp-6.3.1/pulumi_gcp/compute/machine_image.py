# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['MachineImageArgs', 'MachineImage']

@pulumi.input_type
class MachineImageArgs:
    def __init__(__self__, *,
                 source_instance: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 guest_flush: Optional[pulumi.Input[bool]] = None,
                 machine_image_encryption_key: Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MachineImage resource.
        :param pulumi.Input[str] source_instance: The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        :param pulumi.Input[str] description: A text description of the resource.
        :param pulumi.Input[bool] guest_flush: Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
               Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        :param pulumi.Input['MachineImageMachineImageEncryptionKeyArgs'] machine_image_encryption_key: Encrypts the machine image using a customer-supplied encryption key.
               After you encrypt a machine image with a customer-supplied key, you must
               provide the same key if you use the machine image later (e.g. to create a
               instance from the image)
               Structure is documented below.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "source_instance", source_instance)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if guest_flush is not None:
            pulumi.set(__self__, "guest_flush", guest_flush)
        if machine_image_encryption_key is not None:
            pulumi.set(__self__, "machine_image_encryption_key", machine_image_encryption_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="sourceInstance")
    def source_instance(self) -> pulumi.Input[str]:
        """
        The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        """
        return pulumi.get(self, "source_instance")

    @source_instance.setter
    def source_instance(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_instance", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A text description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="guestFlush")
    def guest_flush(self) -> Optional[pulumi.Input[bool]]:
        """
        Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
        Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        """
        return pulumi.get(self, "guest_flush")

    @guest_flush.setter
    def guest_flush(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "guest_flush", value)

    @property
    @pulumi.getter(name="machineImageEncryptionKey")
    def machine_image_encryption_key(self) -> Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']]:
        """
        Encrypts the machine image using a customer-supplied encryption key.
        After you encrypt a machine image with a customer-supplied key, you must
        provide the same key if you use the machine image later (e.g. to create a
        instance from the image)
        Structure is documented below.
        """
        return pulumi.get(self, "machine_image_encryption_key")

    @machine_image_encryption_key.setter
    def machine_image_encryption_key(self, value: Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']]):
        pulumi.set(self, "machine_image_encryption_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _MachineImageState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 guest_flush: Optional[pulumi.Input[bool]] = None,
                 machine_image_encryption_key: Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 source_instance: Optional[pulumi.Input[str]] = None,
                 storage_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering MachineImage resources.
        :param pulumi.Input[str] description: A text description of the resource.
        :param pulumi.Input[bool] guest_flush: Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
               Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        :param pulumi.Input['MachineImageMachineImageEncryptionKeyArgs'] machine_image_encryption_key: Encrypts the machine image using a customer-supplied encryption key.
               After you encrypt a machine image with a customer-supplied key, you must
               provide the same key if you use the machine image later (e.g. to create a
               instance from the image)
               Structure is documented below.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] source_instance: The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] storage_locations: The regional or multi-regional Cloud Storage bucket location where the machine image is stored.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if guest_flush is not None:
            pulumi.set(__self__, "guest_flush", guest_flush)
        if machine_image_encryption_key is not None:
            pulumi.set(__self__, "machine_image_encryption_key", machine_image_encryption_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if source_instance is not None:
            pulumi.set(__self__, "source_instance", source_instance)
        if storage_locations is not None:
            pulumi.set(__self__, "storage_locations", storage_locations)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A text description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="guestFlush")
    def guest_flush(self) -> Optional[pulumi.Input[bool]]:
        """
        Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
        Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        """
        return pulumi.get(self, "guest_flush")

    @guest_flush.setter
    def guest_flush(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "guest_flush", value)

    @property
    @pulumi.getter(name="machineImageEncryptionKey")
    def machine_image_encryption_key(self) -> Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']]:
        """
        Encrypts the machine image using a customer-supplied encryption key.
        After you encrypt a machine image with a customer-supplied key, you must
        provide the same key if you use the machine image later (e.g. to create a
        instance from the image)
        Structure is documented below.
        """
        return pulumi.get(self, "machine_image_encryption_key")

    @machine_image_encryption_key.setter
    def machine_image_encryption_key(self, value: Optional[pulumi.Input['MachineImageMachineImageEncryptionKeyArgs']]):
        pulumi.set(self, "machine_image_encryption_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter(name="sourceInstance")
    def source_instance(self) -> Optional[pulumi.Input[str]]:
        """
        The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        """
        return pulumi.get(self, "source_instance")

    @source_instance.setter
    def source_instance(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_instance", value)

    @property
    @pulumi.getter(name="storageLocations")
    def storage_locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The regional or multi-regional Cloud Storage bucket location where the machine image is stored.
        """
        return pulumi.get(self, "storage_locations")

    @storage_locations.setter
    def storage_locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "storage_locations", value)


class MachineImage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 guest_flush: Optional[pulumi.Input[bool]] = None,
                 machine_image_encryption_key: Optional[pulumi.Input[pulumi.InputType['MachineImageMachineImageEncryptionKeyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_instance: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a Machine Image resource. Machine images store all the configuration,
        metadata, permissions, and data from one or more disks required to create a
        Virtual machine (VM) instance.

        To get more information about MachineImage, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/beta/machineImages)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/compute/docs/machine-images)

        ## Example Usage
        ### Machine Image Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        vm = gcp.compute.Instance("vm",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        image = gcp.compute.MachineImage("image", source_instance=vm.self_link,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Compute Machine Image Kms

        ```python
        import pulumi
        import pulumi_gcp as gcp

        vm = gcp.compute.Instance("vm",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        key_ring = gcp.kms.KeyRing("keyRing", location="us",
        opts=pulumi.ResourceOptions(provider=google_beta))
        crypto_key = gcp.kms.CryptoKey("cryptoKey", key_ring=key_ring.id,
        opts=pulumi.ResourceOptions(provider=google_beta))
        project = gcp.organizations.get_project()
        kms_project_binding = gcp.projects.IAMMember("kms-project-binding",
            project=project.project_id,
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@compute-system.iam.gserviceaccount.com",
            opts=pulumi.ResourceOptions(provider=google_beta))
        image = gcp.compute.MachineImage("image",
            source_instance=vm.self_link,
            machine_image_encryption_key=gcp.compute.MachineImageMachineImageEncryptionKeyArgs(
                kms_key_name=crypto_key.id,
            ),
            opts=pulumi.ResourceOptions(provider=google_beta,
                depends_on=[kms_project_binding]))
        ```

        ## Import

        MachineImage can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default projects/{{project}}/global/machineImages/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default {{project}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A text description of the resource.
        :param pulumi.Input[bool] guest_flush: Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
               Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        :param pulumi.Input[pulumi.InputType['MachineImageMachineImageEncryptionKeyArgs']] machine_image_encryption_key: Encrypts the machine image using a customer-supplied encryption key.
               After you encrypt a machine image with a customer-supplied key, you must
               provide the same key if you use the machine image later (e.g. to create a
               instance from the image)
               Structure is documented below.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_instance: The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MachineImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a Machine Image resource. Machine images store all the configuration,
        metadata, permissions, and data from one or more disks required to create a
        Virtual machine (VM) instance.

        To get more information about MachineImage, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/beta/machineImages)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/compute/docs/machine-images)

        ## Example Usage
        ### Machine Image Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        vm = gcp.compute.Instance("vm",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        image = gcp.compute.MachineImage("image", source_instance=vm.self_link,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```
        ### Compute Machine Image Kms

        ```python
        import pulumi
        import pulumi_gcp as gcp

        vm = gcp.compute.Instance("vm",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-9",
                ),
            ),
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                network="default",
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        key_ring = gcp.kms.KeyRing("keyRing", location="us",
        opts=pulumi.ResourceOptions(provider=google_beta))
        crypto_key = gcp.kms.CryptoKey("cryptoKey", key_ring=key_ring.id,
        opts=pulumi.ResourceOptions(provider=google_beta))
        project = gcp.organizations.get_project()
        kms_project_binding = gcp.projects.IAMMember("kms-project-binding",
            project=project.project_id,
            role="roles/cloudkms.cryptoKeyEncrypterDecrypter",
            member=f"serviceAccount:service-{project.number}@compute-system.iam.gserviceaccount.com",
            opts=pulumi.ResourceOptions(provider=google_beta))
        image = gcp.compute.MachineImage("image",
            source_instance=vm.self_link,
            machine_image_encryption_key=gcp.compute.MachineImageMachineImageEncryptionKeyArgs(
                kms_key_name=crypto_key.id,
            ),
            opts=pulumi.ResourceOptions(provider=google_beta,
                depends_on=[kms_project_binding]))
        ```

        ## Import

        MachineImage can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default projects/{{project}}/global/machineImages/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default {{project}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/machineImage:MachineImage default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param MachineImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 guest_flush: Optional[pulumi.Input[bool]] = None,
                 machine_image_encryption_key: Optional[pulumi.Input[pulumi.InputType['MachineImageMachineImageEncryptionKeyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_instance: Optional[pulumi.Input[str]] = None,
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
            __props__ = MachineImageArgs.__new__(MachineImageArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["guest_flush"] = guest_flush
            __props__.__dict__["machine_image_encryption_key"] = machine_image_encryption_key
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if source_instance is None and not opts.urn:
                raise TypeError("Missing required property 'source_instance'")
            __props__.__dict__["source_instance"] = source_instance
            __props__.__dict__["self_link"] = None
            __props__.__dict__["storage_locations"] = None
        super(MachineImage, __self__).__init__(
            'gcp:compute/machineImage:MachineImage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            guest_flush: Optional[pulumi.Input[bool]] = None,
            machine_image_encryption_key: Optional[pulumi.Input[pulumi.InputType['MachineImageMachineImageEncryptionKeyArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            source_instance: Optional[pulumi.Input[str]] = None,
            storage_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'MachineImage':
        """
        Get an existing MachineImage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A text description of the resource.
        :param pulumi.Input[bool] guest_flush: Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
               Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        :param pulumi.Input[pulumi.InputType['MachineImageMachineImageEncryptionKeyArgs']] machine_image_encryption_key: Encrypts the machine image using a customer-supplied encryption key.
               After you encrypt a machine image with a customer-supplied key, you must
               provide the same key if you use the machine image later (e.g. to create a
               instance from the image)
               Structure is documented below.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] source_instance: The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] storage_locations: The regional or multi-regional Cloud Storage bucket location where the machine image is stored.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MachineImageState.__new__(_MachineImageState)

        __props__.__dict__["description"] = description
        __props__.__dict__["guest_flush"] = guest_flush
        __props__.__dict__["machine_image_encryption_key"] = machine_image_encryption_key
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["source_instance"] = source_instance
        __props__.__dict__["storage_locations"] = storage_locations
        return MachineImage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A text description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="guestFlush")
    def guest_flush(self) -> pulumi.Output[Optional[bool]]:
        """
        Specify this to create an application consistent machine image by informing the OS to prepare for the snapshot process.
        Currently only supported on Windows instances using the Volume Shadow Copy Service (VSS).
        """
        return pulumi.get(self, "guest_flush")

    @property
    @pulumi.getter(name="machineImageEncryptionKey")
    def machine_image_encryption_key(self) -> pulumi.Output[Optional['outputs.MachineImageMachineImageEncryptionKey']]:
        """
        Encrypts the machine image using a customer-supplied encryption key.
        After you encrypt a machine image with a customer-supplied key, you must
        provide the same key if you use the machine image later (e.g. to create a
        instance from the image)
        Structure is documented below.
        """
        return pulumi.get(self, "machine_image_encryption_key")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="sourceInstance")
    def source_instance(self) -> pulumi.Output[str]:
        """
        The source instance used to create the machine image. You can provide this as a partial or full URL to the resource.
        """
        return pulumi.get(self, "source_instance")

    @property
    @pulumi.getter(name="storageLocations")
    def storage_locations(self) -> pulumi.Output[Sequence[str]]:
        """
        The regional or multi-regional Cloud Storage bucket location where the machine image is stored.
        """
        return pulumi.get(self, "storage_locations")

