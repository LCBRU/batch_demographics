import os
from flask import current_app


def save_file(batch, file):
    filepath = batch_file_path(batch)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)


def batch_file_path(batch):
    return os.path.join(
        current_app.config["FILE_UPLOAD_DIRECTORY"], batch.filename
    )
