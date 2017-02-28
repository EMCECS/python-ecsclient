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
