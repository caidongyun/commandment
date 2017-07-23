from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from enum import IntFlag
from .. import models


class ErrorChainItem(Schema):
    LocalizedDescription = fields.String()
    USEnglishDescription = fields.String()
    ErrorDomain = fields.String()
    ErrorCode = fields.Number()


class CommandResponse(Schema):
    Status = fields.String()
    UDID = fields.UUID()
    CommandUUID = fields.UUID()
    ErrorChain = fields.Nested(ErrorChainItem, many=True)




class OrganizationInfo(Schema):
    pass


class AutoSetupAdminAccount(Schema):
    GUID = fields.UUID()
    shortName = fields.String()


class OSUpdateSettings(Schema):
    CatalogURL = fields.String()
    IsDefaultCatalog = fields.Boolean()
    PreviousScanDate = fields.Date()
    PreviousScanResult = fields.String()
    PerformPeriodicCheck = fields.Boolean()
    AutomaticCheckEnabled = fields.Boolean()
    BackgroundDownloadEnabled = fields.Boolean()
    AutomaticAppInstallationEnabled = fields.Boolean()
    AutomaticOSInstallationEnabled = fields.Boolean()
    AutomaticSecurityUpdatesEnabled = fields.Boolean()


class DeviceInformation(Schema):
    # Table 5
    UDID = fields.String(attribute='udid')
    # Languages
    DeviceID = fields.String(attribute='device_id')
    OrganizationInfo = fields.Nested(OrganizationInfo)
    LastCloudBackupDate = fields.Date(attribute='last_cloud_backup_date')
    AwaitingConfiguration = fields.Boolean(attribute='awaiting_configuration')
    AutoSetupAdminAccounts = fields.Nested(AutoSetupAdminAccount, many=True)

    # Table 6
    iTunesStoreAccountIsActive = fields.Boolean(attribute='itunes_store_account_is_active')
    iTunesStoreAccountHash = fields.String(attribute='itunes_store_account_hash')

    # Table 7
    DeviceName = fields.String(attribute='device_name')
    OSVersion = fields.String(attribute='os_version')
    BuildVersion = fields.String(attribute='build_version')
    ModelName = fields.String(attribute='model_name')
    Model = fields.String(attribute='model')
    ProductName = fields.String(attribute='product_name')
    SerialNumber = fields.String(attribute='serial_number')
    DeviceCapacity = fields.Float(attribute='device_capacity')
    AvailableDeviceCapacity = fields.Float(attribute='available_device_capacity')
    BatteryLevel = fields.Float(attribute='battery_level')
    CellularTechnology = fields.Integer(attribute='cellular_technology')
    IMEI = fields.String(attribute='imei')
    MEID = fields.String(attribute='meid')
    ModemFirmwareVersion = fields.String(attribute='modem_firmware_version')
    IsSupervised = fields.Boolean(attribute='is_supervised')
    IsDeviceLocatorServiceEnabled = fields.Boolean(attribute='is_device_locator_service_enabled')
    IsActivationLockEnabled = fields.Boolean(attribute='is_activation_lock_enabled')
    IsDoNotDisturbInEffect = fields.Boolean(attribute='is_do_not_disturb_in_effect')
    EASDeviceIdentifier = fields.String(attribute='eas_device_identifier')
    IsCloudBackupEnabled = fields.Boolean(attribute='is_cloud_backup_enabled')
    OSUpdateSettings = fields.Nested(OSUpdateSettings, attribute='os_update_settings')  # T8
    LocalHostName = fields.String(attribute='local_hostname')
    HostName = fields.String(attribute='hostname')
    SystemIntegrityProtectionEnabled = fields.Boolean(attribute='sip_enabled')
    # Array of str
    #ActiveManagedUsers = fields.Nested(ActiveManagedUser)
    IsMDMLostModeEnabled = fields.Boolean(attribute='is_mdm_lost_mode_enabled')
    MaximumResidentUsers = fields.Integer(attribute='maximum_resident_users')

    # Table 9
    ICCID = fields.String(attribute='iccid')
    BluetoothMAC = fields.String(attribute='bluetooth_mac')
    WiFiMAC = fields.String(attribute='wifi_mac')
    EthernetMACs = fields.String(attribute='ethernet_macs', many=True)
    CurrentCarrierNetwork = fields.String(attribute='current_carrier_network')
    SIMCarrierNetwork = fields.String(attribute='sim_carrier_network')
    SubscriberCarrierNetwork = fields.String(attribute='subscriber_carrier_network')
    CarrierSettingsVersion = fields.String(attribute='carrier_settings_version')
    PhoneNumber = fields.String(attribute='phone_number')
    VoiceRoamingEnabled = fields.Boolean(attribute='voice_roaming_enabled')
    DataRoamingEnabled = fields.Boolean(attribute='data_roaming_enabled')
    IsRoaming = fields.Boolean(attribute='is_roaming')
    PersonalHotspotEnabled = fields.Boolean(attribute='personal_hotspot_enabled')
    SubscriberMCC = fields.String(attribute='subscriber_mcc')
    SubscriberMNC = fields.String(attribute='subscriber_mnc')
    CurrentMCC = fields.String(attribute='current_mcc')
    CurrentMNC = fields.String(attribute='current_mnc')

    # @post_load
    # def make_device(self, data):
    #     return models.Device(**data)


class DeviceInformationResponse(CommandResponse):
    QueryResponses = fields.Nested(DeviceInformation)


class HardwareEncryptionCaps(IntFlag):
    Nothing = 0
    BlockLevelEncryption = 1
    FileLevelEncryption = 2

    All = BlockLevelEncryption | FileLevelEncryption


class FirewallApplicationItem(Schema):
    BundleID = fields.String()
    Allowed = fields.Boolean()
    Name = fields.String()


class FirewallSettings(Schema):
    FirewallEnabled = fields.Boolean()
    BlockAllIncoming = fields.Boolean()
    StealthMode = fields.Boolean()
    Applications = fields.Nested(FirewallApplicationItem, many=True)


class SecurityInfoResponse(CommandResponse):
    HardwareEncryptionCaps = EnumField(HardwareEncryptionCaps)
    PasscodePresent = fields.Boolean()
    PasscodeCompliant = fields.Boolean()
    PasscodeCompliantWithProfiles = fields.Boolean()
    PasscodeLockGracePeriodEnforced = fields.Integer()
    FDE_Enabled = fields.Boolean()
    FDE_HasPersonalRecoveryKey = fields.Boolean()
    FDE_HasInstitutionalRecoveryKey = fields.Boolean()
    FirewallSettings = fields.Nested(FirewallSettings)
    SystemIntegrityProtectionEnabled = fields.Boolean()


class InstalledApplication(Schema):
    Identifier = fields.String(attribute='bundle_identifier')
    Version = fields.String(attribute='version')
    ShortVersion = fields.String(attribute='short_version')
    Name = fields.String(attribute='name')
    BundleSize = fields.Integer(attribute='bundle_size')
    DynamicSize = fields.Integer(attribute='dynamic_size')
    IsValidated = fields.Boolean(attribute='is_validated')

    @post_load
    def make_installed_application(self, data: dict) -> models.InstalledApplication:
        return models.InstalledApplication(**data)


class InstalledApplicationListResponse(CommandResponse):
    InstalledApplicationList = fields.Nested(InstalledApplication, many=True)


class CertificateListItem(Schema):
    CommonName = fields.String()
    IsIdentity = fields.Boolean()
    Data = fields.String()

    @post_load
    def make_installed_certificate(self, data: dict) -> models.InstalledCertificate:
        return models.InstalledCertificate(**data)


class CertificateListResponse(CommandResponse):
    CertificateList = fields.Nested(CertificateListItem, many=True)


class AvailableOSUpdate(Schema):
    AllowsInstallLater = fields.Boolean(attribute='allows_install_later')
    AppIdentifiersToClose = fields.List(fields.String, attribute='app_identifiers_to_close', many=True)
    HumanReadableName = fields.String(attribute='human_readable_name')
    HumanReadableNameLocale = fields.String(attribute='human_readable_name_locale')
    IsConfigDataUpdate = fields.Boolean(attribute='is_config_data_update')
    IsCritical = fields.Boolean(attribute='is_critical')
    IsFirmwareUpdate = fields.Boolean(attribute='is_firmware_update')
    MetadataURL = fields.String(attribute='metadata_url')
    ProductKey = fields.String(attribute='product_key')
    RestartRequired = fields.Boolean(attribute='restart_required')
    Version = fields.String(attribute='version')

    @post_load
    def make_available_os_update(self, data: dict) -> models.AvailableOSUpdate:
        return models.AvailableOSUpdate(**data)


class AvailableOSUpdateListResponse(CommandResponse):
    AvailableOSUpdates = fields.Nested(AvailableOSUpdate, many=True)


class ProfileListPayloadItem(Schema):
    PayloadDescription = fields.String(attribute='description')
    PayloadDisplayName = fields.String(attribute='display_name')
    PayloadIdentifier = fields.String(attribute='identifier')
    PayloadOrganization = fields.String(attribute='organization')
    PayloadType = fields.String(attribute='payload_type')
    PayloadUUID = fields.UUID(attribute='uuid')
    # PayloadVersion = fields.Integer(attribute='payload_version')

    @post_load
    def make_installed_payload(self, data: dict) -> models.InstalledPayload:
        return models.InstalledPayload(**data)


class ProfileListItem(Schema):
    HasRemovalPasscode = fields.Boolean(attribute='has_removal_password')
    IsEncrypted = fields.Boolean(attribute='is_encrypted')
    PayloadDescription = fields.String(attribute='payload_description')
    PayloadDisplayName = fields.String(attribute='payload_display_name')
    PayloadIdentifier = fields.String(attribute='payload_identifier')
    PayloadOrganization = fields.String(attribute='payload_organization')
    PayloadRemovalDisallowed = fields.Boolean(attribute='payload_removal_disallowed')
    PayloadUUID = fields.UUID(attribute='payload_uuid')
    # PayloadVersion = fields.Integer(attribute='payload_version')
    #SignerCertificates = fields.Nested(attribute='signer_certificates', many=True)
    PayloadContent = fields.Nested(ProfileListPayloadItem, attribute='payload_content', many=True)

    @post_load
    def make_installed_profile(self, data: dict) -> models.InstalledProfile:
        return models.InstalledProfile(**data)


class ProfileListResponse(CommandResponse):
    ProfileList = fields.Nested(ProfileListItem, many=True)