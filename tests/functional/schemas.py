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
                    "link": {
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
        "link": {
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
