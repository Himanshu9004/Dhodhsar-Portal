import logging
from datetime import datetime, timezone

from pymongo.errors import ConnectionFailure, OperationFailure
from werkzeug.security import generate_password_hash

from app.models import COLLECTION_SCHEMAS

logger = logging.getLogger(__name__)


def initialize_database(mongo, app):
    try:
        db = mongo.db
        existing_collections = set(db.list_collection_names())

        for collection_name in COLLECTION_SCHEMAS:
            if collection_name not in existing_collections:
                db.create_collection(collection_name)

        db.admins.create_index("username", unique=True)
        db.notices.create_index([("created_at", -1)])
        db.contacts.create_index([("created_at", -1)])
        db.grievances.create_index([("created_at", -1)])
        db.mandi_rates.create_index([("updated_at", -1)])
        db.businesses.create_index([("approved", 1), ("created_at", -1)])
        db.works.create_index([("created_at", -1)])
        db.schemes.create_index([("created_at", -1)])
        db.jobs.create_index([("created_at", -1)])

        admin_username = app.config.get("ADMIN_USERNAME")
        admin_password = app.config.get("ADMIN_PASSWORD")
        if not db.admins.find_one({"username": admin_username}):
            db.admins.insert_one(
                {
                    "username": admin_username,
                    "password": generate_password_hash(admin_password),
                    "role": "super_admin",
                    "created_at": datetime.now(timezone.utc),
                }
            )
        return True
    except (ConnectionFailure, OperationFailure) as exc:
        logger.warning("MongoDB is not reachable; skipping DB initialization: %s", exc)
        return False
