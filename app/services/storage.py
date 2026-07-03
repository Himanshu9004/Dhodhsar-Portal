import os
import uuid

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file_storage, upload_folder):
    if file_storage and allowed_file(file_storage.filename):
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(file_storage.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        upload_path = os.path.join(upload_folder, unique_name)
        file_storage.save(upload_path)
        return os.path.join("uploads", unique_name)
    return None
