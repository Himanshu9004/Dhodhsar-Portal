from datetime import datetime, timezone


COLLECTION_SCHEMAS = {
    "admins": {
        "username": {"type": "string", "required": True, "unique": True},
        "password": {"type": "string", "required": True},
        "role": {"type": "string", "default": "super_admin"},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "notices": {
        "title": {"type": "string", "required": True},
        "body": {"type": "string", "required": True},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "contacts": {
        "name": {"type": "string", "required": True},
        "phone": {"type": "string", "required": True},
        "role": {"type": "string", "required": True},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "grievances": {
        "name": {"type": "string", "required": True},
        "phone": {"type": "string", "required": True},
        "subject": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "status": {"type": "string", "default": "new"},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "mandi_rates": {
        "crop": {"type": "string", "required": True},
        "price": {"type": "string", "required": True},
        "unit": {"type": "string", "default": "quintal"},
        "updated_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "businesses": {
        "name": {"type": "string", "required": True},
        "category": {"type": "string", "required": True},
        "phone": {"type": "string", "required": True},
        "address": {"type": "string", "required": True},
        "approved": {"type": "bool", "default": False},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "works": {
        "title": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "budget_status": {"type": "string", "required": True},
        "image": {"type": "string", "required": False},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "schemes": {
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "link": {"type": "string", "required": False},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
    "jobs": {
        "title": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "link": {"type": "string", "required": False},
        "created_at": {"type": "datetime", "default": "datetime.now(timezone.utc)"},
    },
}


def get_collection_schemas():
    return COLLECTION_SCHEMAS
