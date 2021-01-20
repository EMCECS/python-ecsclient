WHOAMI = {
    "type": "object",
    "properties": {
        "namespace": {"type": "string"},
        "last_time_password_changed": {
            "type": "string",
            "format": "date-time"
        },
        "distinguished_name": {"type": "string"},
        "common_name": {"type": "string"},
        "roles": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": [
        "namespace",
        "last_time_password_changed",
        "distinguished_name",
        "common_name",
        "roles",
    ]
}

LINK = {
    "type": "object",
    "properties": {
        "rel": {"type": "string"},
        "href": {"type": "string"}
    },
    "required": [
        "rel",
        "href"
    ]
}

NAMESPACES = {
    "type": "object",
    "properties": {
        "namespace": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "link": LINK
                },
                "required": [
                    "id",
                    "name",
                    "link"
                ]
            },
        }
    },
    "required": [
        "namespace"
    ]
}

TENANTS = {
    "type": "object",
    "properties": {
        "tenant": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                },
                "required": [
                    "id",
                ]
            },
        }
    },
    "required": ["tenant"]
}
TENANT = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
    },
    "required": ["id"]
}

NAMESPACE = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "id": {"type": "string"},
        "inactive": {"type": "boolean"},
        "is_stale_allowed": {"type": "boolean"},
        "is_encryption_enabled": {"type": ["string", "boolean"]},  # Workaround: The API returns a string instead of
        # a boolean
        "is_compliance_enabled": {"type": "boolean"},
        "global": {"type": ["string", "null"]},
        "remote": {"type": ["string", "null"]},
        "vdc": {"type": ["string", "null"]},
        "default_data_services_vpool": {"type": "string"},
        "allowed_vpools_list": {"type": "array"},
        "disallowed_vpools_list": {"type": "array"},
        "default_bucket_block_size": {"type": "number"},
        "user_mapping": {"type": "array"},
        "link": LINK
    },
    "required": [
        "name",
        "id",
        "inactive",
        "is_stale_allowed",
        "is_encryption_enabled",
        "is_compliance_enabled",
        "global",
        "remote",
        "vdc",
        "default_data_services_vpool",
        "allowed_vpools_list",
        "disallowed_vpools_list",
        "default_bucket_block_size",
        "user_mapping",
        "link"
    ]
}

CERTIFICATE = {
    "type": "object",
    "properties": {
        "chain": {"type": "string"}
    },
    "required": [
        "chain",
    ]
}

LICENSE = {
    "type": "object",
    "properties": {
        "license_feature": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "product": {"type": "string"},
                    "version": {"type": "string"},
                    "model": {"type": "string"},
                    "licensed_ind": {"type": "boolean"},
                    "trial_license_ind": {"type": "boolean"},
                    "storage_capacity": {"type": "string"},
                    "notice": {"type": "string"},
                    "serial": {"type": "string"},
                    "expired_ind": {"type": "boolean"},
                    "issued_date": {"type": "string", "format": "date-time"},
                    "license_id_indicator": {"type": "string"},
                    "issuer": {"type": "string"},
                    "site_id": {"type": "string"}
                },
                "required": [
                    "product",
                    "version",
                    "model",
                    "licensed_ind",
                    "trial_license_ind",
                    "storage_capacity",
                    "notice",
                    "serial",
                    "expired_ind",
                    "issued_date",
                    "license_id_indicator",
                    "issuer",
                    "site_id"
                ]
            },
        },
        "license_text": {"type": "string"}
    },
    "required": [
        "license_feature",
        "license_text"
    ]
}

STORAGE_POOL = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "isProtected": {"type": "boolean"},
        "isColdStorageEnabled": {"type": "boolean"}
    },
    "required": [
        "id",
        "name",
        "isProtected",
        "isColdStorageEnabled"
    ]
}

STORAGE_POOLS = {
    "type": "object",
    "properties": {
        "varray": {
            "type": "array",
            "minItems": 1,
            "items": STORAGE_POOL
        }
    },
    "required": [
        "varray"
    ]
}

VDC = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "vdcId": {"type": "string"},
        "name": {"type": "string"},
        "vdcName": {"type": "string"},
        "link": LINK,
        "inactive": {"type": "boolean"},
        "local": {"type": "boolean"},
        "global": {"type": ["boolean", "null"]},
        "remote": {"type": ["boolean", "null"]},
        "vdc": {
            "type": ["object", "null"],
            "properties": {
                "id": {"type": "string"},
                "link": {"type": "string"}
            },
            "required": [
                "id",
                "link"
            ]
        },
        "is_encryption_enabled": {"type": "boolean"},
        "managementEndPoints": {"type": "string"},
        "interVdcEndPoints": {"type": "string"},
        "interVdcCmdEndPoints": {"type": "string"},
        "secretKeys": {"type": "string"},
        "permanentlyFailed": {"type": "boolean"}
    },
    "required": [
        "id",
        "vdcId",
        "name",
        "vdcName",
        "link",
        "inactive",
        "local",
        "global",
        "remote",
        "vdc",
        "is_encryption_enabled",
        "managementEndPoints",
        "interVdcEndPoints",
        "interVdcCmdEndPoints",
        "secretKeys",
        "permanentlyFailed"
    ]
}

VDCS = {
    "type": "object",
    "properties": {
        "vdc": {
            "type": "array",
            "minItems": 1,
            "items": VDC
        }
    },
    "required": [
        "vdc"
    ]
}

REPLICATION_GROUP = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "inactive": {"type": "boolean"},
        "global": {"type": ["boolean", "null"]},
        "remote": {"type": ["boolean", "null"]},
        "vdc": {
            "type": ["object", "null"],
            "properties": {
                "id": {"type": "string"},
                "link": {"type": "string"}
            },
            "required": [
                "id",
                "link"
            ]
        },
        "description": {"type": "string"},
        "varrayMappings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": [
                    "name",
                    "value"
                ]
            }
        },
        "creation_time": {"type": "number"},
        "isAllowAllNamespaces": {"type": "boolean"},
        "enable_rebalancing": {"type": "boolean"},
        "isFullRep": {"type": "boolean"}
    },
    "required": [
        "id",
        "name",
        "global",
        "remote",
        "vdc",
        "description",
        "varrayMappings",
        "isAllowAllNamespaces",
        "enable_rebalancing",
        "isFullRep"
    ]
}

REPLICATION_GROUPS = {
    "type": "object",
    "properties": {
        "data_service_vpool": {
            "type": "array",
            "minItems": 1,
            "items": REPLICATION_GROUP
        }
    },
    "required": [
        "data_service_vpool"
    ]
}

DATA_STORES = {
    "type": "object",
    "properties": {
        "data_store": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "resource_type": {"type": "string"},
                    "link": LINK
                },
                "required": [
                    "id",
                    "name",
                    "resource_type",
                    "link"
                ]
            }
        }
    },
    "required": [
        "data_store"
    ]
}

DATA_STORE = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "link": LINK,
        "remote": {"type": ["boolean", "null"]},
        "global": {"type": ["boolean", "null"]},
        "vdc": {"type": ["string", "null"]},
        "creation_time": {"type": "number"},
        "device_info": {"type": "string"},
        "varray": {"type": "string"},
        "device_state": {"type": "string"},
        "usable_gb": {"type": "number"},
        "used_gb": {"type": "number"},
        "free_gb": {"type": "number"}
    },
    "required": [
        "id",
        "name",
        "description",
        "link",
        "remote",
        "global",
        "vdc",
        "creation_time",
        "device_info",
        "varray",
        "device_state",
        "usable_gb",
        "used_gb",
        "free_gb"
    ]
}

DATA_STORES_COMMODITY = {
    "type": "object",
    "properties": {
        "commodity_data_store": {
            "type": "array",
            "minItems": 1,
            "items": DATA_STORE
        }
    },
    "required": [
        "commodity_data_store"
    ]
}

DATA_STORE_TASK = {
    "type": "object",
    "properties": {
        "op_id": {"type": "string"},
        "resource": {
            "type": "object",
            "properties": {
                "link": LINK,
                "id": {"type": "string"},
                "name": {"type": "string"}
            },
            "required": [
                "link",
                "id",
                "name"
            ]
        },
        "name": {"type": "string"},
        "remote": {"type": ["boolean", "null"]},
        "global": {"type": ["boolean", "null"]},
        "vdc": {"type": ["string", "null"]},
        "link": LINK,
        "restLink": {"type": ["object", "null"]},
        "state": {"type": "string"},
        "associated_resources": {"type": "array"}
    },
    "required": [
        "op_id",
        "resource",
        "name",
        "global",
        "remote",
        "vdc",
        "link",
        "restLink",
        "state",
        "associated_resources",
    ]
}

DATA_STORE_TASKS = {
    "type": "object",
    "properties": {
        "task": {
            "type": "array",
            "minItems": 1,
            "items": DATA_STORE_TASK
        }
    },
    "required": [
        "task"
    ]
}

OBJECT_USER = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "created": {
            "type": "string",
            "format": "date-time"
        },
        "namespace": {"type": "string"},
        "locked": {"type": "boolean"}
    },
    "required": [
        "name",
        "created",
        "namespace",
        "locked"
    ]
}

OBJECT_USER_2 = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "namespace": {"type": "string"},
    },
    "required": [
        "userid",
        "namespace"
    ]
}

OBJECT_USERS = {
    "type": "object",
    "properties": {
        "blobuser": {
            "type": "array",
            "minItems": 0,
            "items": OBJECT_USER_2
        },
        "Filter": {"type": "string"}
    },
    "required": [
        "blobuser"
    ]
}

SECRET_KEYS = {
    "type": "object",
    "properties": {
        "secret_key_1": {"type": "string"},
        "secret_key_2": {"type": "string"},
        "key_timestamp_1": {"type": "string"},
        "key_timestamp_2": {"type": "string"},
        "key_expiry_timestamp_1": {"type": "string"},
        "key_expiry_timestamp_2": {"type": "string"},
        "link": LINK
    },
    "required": [
        "secret_key_1",
        "secret_key_2",
        "key_timestamp_1",
        "key_timestamp_2"
    ]
}

SECRET_KEY = {
    "type": "object",
    "properties": {
        "secret_key": {"type": "string"},
        "key_timestamp": {"type": "string"},
        "key_expiry_timestamp": {"type": "string"},
        "link": LINK
    },
    "required": [
        "secret_key",
        "key_timestamp",
        "key_expiry_timestamp",
        "link"
    ]
}

BUCKET_SHORT = {
    "type": "object",
    "properties": {
        "TagSet": {"type": "array"},
        "id": {"type": "string"},
        "global": {"type": ["boolean", "null"]},
        "vdc": {"type": ["string", "null"]},
        "inactive": {"type": "boolean"},
        "metaData": {
            "type": "object",
            "properties": {
                "search_enabled": {"type": "boolean"},
                "max_keys": {"type": "number"},
                "metadata": {"type": "array"}
            },
            "required": [
                "search_enabled",
                "max_keys",
                "metadata"
            ]
        },
        "remote": {"type": ["boolean", "null"]},
        "name": {"type": "string"}
    },
    "required": [
        "TagSet",
        "global",
        "vdc",
        "inactive",
        "metaData",
        "remote",
        "name"
    ]
}

BUCKET = {
    "type": "object",
    "properties": {
        "TagSet": {"type": "array"},
        "id": {"type": "string"},
        "global": {"type": ["boolean", "null"]},
        "vdc": {"type": ["string", "null"]},
        "search_metadata": {
            "type": "object",
            "properties": {
                "search_enabled": {"type": "boolean"},
                "max_keys": {"type": "number"},
                "metadata": {"type": "array"}
            },
            "required": [
                "search_enabled",
                "max_keys",
                "metadata"
            ]
        },
        "remote": {"type": ["boolean", "null"]},
        "name": {"type": "string"},
        "block_size": {"type": "number"},
        "retention": {"type": "number"},
        "api_type": {"type": "string"},
        "notification_size": {"type": "number"},
        "namespace": {"type": "string"},
        "default_retention": {"type": "number"},
        "locked": {"type": "boolean"},
        "is_encryption_enabled": {"type": ["boolean", "string"]},
        "is_stale_allowed": {"type": "boolean"},
        "vpool": {"type": "string"},
        "fs_access_enabled": {"type": "boolean"},
        "created": {"type": "string", "format": "date-time"},
        "owner": {"type": "string"}
    },
    "required": [
        "TagSet",
        "global",
        "vdc",
        "search_metadata",
        "remote",
        "name",
        "block_size",
        "retention",
        "api_type",
        "notification_size",
        "namespace",
        "default_retention",
        "locked",
        "is_encryption_enabled",
        "is_stale_allowed",
        "vpool",
        "fs_access_enabled",
        "created",
        "owner"
    ]
}

BUCKET_LIST = {
    "type": "object",
    "properties": {
        "object_bucket": {
            "type": "array",
            "minItems": 0,
            "items": BUCKET
        },
        "Filter": {"type": "string"},
        "MaxBuckets": {"type": "number"}
    },
    "required": [
        "object_bucket",
        "Filter",
        "MaxBuckets"
    ]
}

BUCKET_ACL = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "properties": {
            "display_name": {"type": "string"},
            "description": {"type": "string"},
            "id": {"type": "string"}
        },
        "required": [
            "display_name",
            "id"
        ]
    }
}

BUCKET_ACL_PERMISSIONS = {
    "type": "object",
    "properties": {
        "permission": BUCKET_ACL
    },
    "required": [
        "permission"
    ]
}

BUCKET_ACL_GROUPS = {
    "type": "object",
    "properties": {
        "group": BUCKET_ACL
    },
    "required": [
        "group"
    ]
}

BUCKET_USER_METADATA = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": [
                    "name",
                    "value"
                ]
            }
        },
        "head_type": {"type": "string"}
    },
    "required": [
        "metadata",
        "head_type"
    ]
}

BUCKET_SYSTEM_METADATA = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "datatype": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": [
                    "name",
                    "datatype",
                    "type"
                ]
            }
        },
        "max_keys": {"type": "number"}
    },
    "required": [
        "metadata",
        "max_keys"
    ]
}

MANAGEMENT_USER = {
    "type": "object",
    "properties": {
        "userId": {"type": "string"},
        "isSystemAdmin": {"type": "boolean"},
        "isSecurityAdmin": {"type": "boolean"},
        "isSystemMonitor": {"type": "boolean"},
        "is_external_group": {"type": "boolean"}
    },
    "required": [
        "userId",
        "isSystemAdmin",
        "isSystemMonitor",
        "is_external_group"
    ]
}

MANAGEMENT_USERS = {
    "type": "object",
    "properties": {
        "mgmt_user_info": {
            "type": "array",
            "minItems": 0,
            "items": MANAGEMENT_USER
        },
    },
    "required": [
        "mgmt_user_info"
    ]
}

GROUP_LIST = {
    "type": "object",
    "properties": {
        "groups_list": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": [
        "groups_list"
    ]
}

VDC_KEYSTORE = {
    "type": "object",
    "properties": {
        "chain": {"type": "string"}
    },
    "required": [
        "chain"
    ]
}

NODE = {
    "type": "object",
    "properties": {
        "rackId": {"type": "string"},
        "version": {"type": "string"},
        "nodeid": {"type": "string"},
        "isLocal": {"type": "boolean"},
        "nodename": {"type": "string"},
        "ip": {"type": "string"},
    },
    "required": [
        "rackId",
        "version",
        "nodeid",
        "isLocal",
        "nodename",
        "ip"
    ]
}

NODE_LIST = {
    "type": "object",
    "properties": {
        "node": {
            "type": "array",
            "items": NODE,
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": [
        "node"
    ]
}

ALERTS = {
    "type": "object",
    "properties": {
        "MaxAlerts": {"type": "number"},
        "Filter": {"type": "string"},
        "alert": {"type": "array"}
    },
    "required": [
        "MaxAlerts",
        "Filter",
        "alert"
    ]
}

CAPACITY = {
    "type": "object",
    "properties": {
        "totalFree_gb": {"type": "number"},
        "totalProvisioned_gb": {"type": "number"}
    },
    "required": [
        "totalFree_gb",
        "totalProvisioned_gb"
    ]
}
