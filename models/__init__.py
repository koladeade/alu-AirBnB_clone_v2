#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
import os
from dotenv import load_dotenv

load_dotenv()

storage_type = os.getenv('HBNB_TYPE_STORAGE')
print(f"HBNB_TYPE_STORAGE: {storage_type}")  # Debugging line to print the storage type

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()