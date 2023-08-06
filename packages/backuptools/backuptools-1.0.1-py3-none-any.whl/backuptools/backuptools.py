import datetime
import json
import os
import pprint
import sys
import tarfile
from abc import ABC, abstractmethod
from typing import List

from .googledriveclient import GoogleDriveClient
from .type import FileNotFoundException


class BackupResource(ABC):

    @abstractmethod
    def backup(self, version: str):
        pass

    @abstractmethod
    def restore(self, version: str):
        pass


class GoogleDriveBackupResource(BackupResource):

    default_local_backup_folder_path = '/data/backups'

    def __init__(self, name: str = None, local_resource_path: str = None, drive_credentials: str = None, drive_root_id: str = None, drive_backup_folder_path: str = None, drive_backup_folder_id: str = None, local_backup_folder_path: str = None, remove_after_backup: bool = False, remove_after_restore: bool = False):
        self.name = name
        self.local_resource_path = os.path.abspath(local_resource_path)

        self.drive_credentials = drive_credentials
        self.drive_root_id = drive_root_id
        self.drive_backup_folder_path = drive_backup_folder_path
        self.drive_backup_folder_id = drive_backup_folder_id

        self.remove_after_backup = remove_after_backup
        self.remove_after_restore = remove_after_restore

        self.local_backup_folder_path = os.path.abspath(
            local_backup_folder_path) if local_backup_folder_path is not None else self.default_local_backup_folder_path

        self._drive_client: GoogleDriveClient = None

        self._prepare_folder()

    def _prepare_folder(self):
        if os.path.exists(self.local_backup_folder_path):
            if not os.path.isdir(self.local_backup_folder_path):
                raise Exception('local_backup_folder_path "{0}" is not folder')
        else:
            os.makedirs(self.local_backup_folder_path)

    @property
    def drive_client(self):
        if self._drive_client is None:
            self._drive_client = GoogleDriveClient(root_id=self.drive_root_id)
            self._drive_client.connect(self.drive_credentials)

        return self._drive_client

    def generate_version_key(self):
        now = datetime.datetime.now()
        version = '{0}-{1:0>2}-{2:0>2}-{3:0>2}-{4:0>2}-{5:0>2}'.format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        return version

    def get_backup_file_name(self, version: str) -> str:
        return '{0}-{1}.tar.gz'.format(self.name, version)

    def get_version_from_backup_file_name(self, file_name: str) -> str:
        prefix = '{0}-'.format(self.name)
        suffix = '.tar.gz'

        if not file_name.startswith(prefix):
            raise ValueError('"{0}" is not correct format'.format(file_name))

        if not file_name.endswith(suffix):
            raise ValueError('"{0}" is not correct format'.format(file_name))

        return file_name[len(prefix): len(file_name) - len(suffix)]

    def get_local_backup_file_path(self, version: str) -> str:
        return os.path.join(self.local_backup_folder_path, self.get_backup_file_name(version))

    def get_drive_backup_file_path(self, version: str) -> str:
        return os.path.join(self.drive_backup_folder_path, self.get_backup_file_name(version))

    def create_version(self, version: str = None):
        version = version or self.generate_version_key()
        file_path = self.get_local_backup_file_path(version)
        with tarfile.open(file_path, 'w:gz') as tar:
            tar.add(self.local_resource_path,
                    arcname=os.path.basename(self.local_resource_path))

        print('Create backup file: "{0}"'.format(file_path))
        return version

    def extract_version(self, version: str):
        file_path = self.get_local_backup_file_path(version)
        print('Extract backup file: "{0}"'.format(file_path))
        source_folder = os.path.dirname(self.local_resource_path)
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(source_folder)

    def upload_version(self, version: str):
        self.drive_client.upload_file(local_file_path=self.get_local_backup_file_path(
            version), drive_folder_path=self.drive_backup_folder_path)

    def download_version(self, version: str):
        self.drive_client.download_file_by_path(drive_file_path=self.get_drive_backup_file_path(
            version), local_folder_path=self.local_backup_folder_path)

    def upload_all(self) -> List[str]:
        # Get list local and remote version
        local_versions = self.list_local_version()
        remote_versions = self.list_drive_version()
        # Filter version need upload
        need_upload_versions = list(set(local_versions) - set(remote_versions))
        # Upload versions
        for version in need_upload_versions:
            self.upload_version(version)

        return need_upload_versions

    def download_all(self):
        # Get list local and remote version
        local_versions = self.list_local_version()
        remote_versions = self.list_drive_version()
        # Filter version need upload
        need_download_versions = list(
            set(remote_versions) - set(local_versions))
        # Upload versions
        for version in need_download_versions:
            self.download_version(version)

        return need_download_versions

    def sync(self):
        uploaded_versions = self.upload_all()
        downloaded_versions = self.download_all()
        return (uploaded_versions, downloaded_versions)

    def backup(self, version: str = None):

        version = version or self.generate_version_key()

        self.create_version(version)
        self.upload_version(version)
        if self.remove_after_backup:
            self.remove_local_version(version)

        return version

    def restore(self, version):
        self.download_version(version)
        self.extract_version(version)
        if self.remove_after_restore:
            self.remove_local_version(version)

    def list_local_version(self) -> List[str]:
        file_names = [f for f in os.listdir(self.local_backup_folder_path) if os.path.isfile(
            os.path.join(self.local_backup_folder_path, f))]
        return [self.get_version_from_backup_file_name(file_name) for file_name in file_names]

    def list_drive_version(self):
        try:
            files = self.drive_client.get_list_file(
                parent_path=self.drive_backup_folder_path)
            file_names = [file['name'] for file in files]
            return [self.get_version_from_backup_file_name(file_name) for file_name in file_names]
        except FileNotFoundException:
            return []

    def remove_local_version(self, version: str):
        backup_path = self.get_local_backup_file_path(version)
        os.remove(backup_path)

    def remove_drive_version(self, version: str):
        backup_path = self.get_drive_backup_file_path(version)
        self.drive_client.rm_by_path_if_exist(backup_path)


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


class BackupTools():

    def __init__(self, config: dict):

        self.resources: list = []
        self.config = config

        self.drive_credentials = self.config.get('drive_credentials')
        self.drive_root_id = self.config.get('drive_root_id')

        self._build_resources()

    def _get_resource(self, data):
        resource_type = data.get('type')
        resource_name = data.get('name')
        resource_args = data.get('args')
        if resource_type == 'GoogleDriveBackupResource':
            resource_args['drive_credentials'] = resource_args.get(
                'drive_credentials') or self.drive_credentials

            resource_args['drive_root_id'] = resource_args.get(
                'drive_root_id') or self.drive_root_id

            return GoogleDriveBackupResource(name=resource_name, **resource_args)

    def _build_resources(self):
        self.resources = [self._get_resource(
            item) for item in self.config.get('resources')]

    def exec(self, *args):

        resource_name = None
        method_name = None
        method_args = None
        resource = None
        method = None

        if len(args) == 0:
            return self.config

        resource_name = args[0]
        resource = next(
            (item for item in self.resources if item.name == resource_name), None)
        if resource is None:
            raise Exception(
                'Resource "{0}" not found'.format(resource_name))

        method_name = args[1]

        method = getattr(resource, method_name)
        if method is None:
            raise Exception('Method "{0}.{1}" not found'.format(
                resource_name, method_name))

        if not callable(method):
            raise Exception('Method "{0}.{1}" not callable'.format(
                resource_name, method_name))

        method_args = args[2:]

        return method(*method_args)
