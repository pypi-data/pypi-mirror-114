# backup-tools

Backup, restore, version control local data to google drive

# Prerequisites

- Python >= 3.6

# Install

```bash
pip install backuptools
```

# Usage

## Create config file

1. Create and download google account service json file `credentials.json` for **google drive service**
2. Share Google Drive folder for Service Account email
3. Get `id` of Google Drive folder and put to `backuptools.config.json` below
4. Create `backuptools.config.json` with content:

```json
{
  "drive_credentials": "<path/to/credentials.json>",
  "drive_root_id": "<id_of_drive_folder>",
  "resources": [
    {
      "type": "GoogleDriveBackupResource",
      "name": "<resource_name>",
      "args": {
        "local_resource_path": "<path/to/local/source>",
        "local_backup_folder_path": "<path/to/local/backup/folder>",
        "drive_backup_folder_path": "<path/to/drive/backup/folder>"
      }
    }
  ]
}
```

## Backup

With auto name

```bash
backuptools -R <resource> backup
```

With specific name

```bash
backuptools -R <resource> backup <version>
```

## Restore

```bash
backuptools -R <resource> restore <version>
```

## List version

List all local and remote version

```bash
backuptools -R <resource> ls
```

List local only version

```bash
backuptools -R <resource> ls --local
```

List remote only version

```bash
backuptools -R <resource> ls --remote
```

## Create local version

With auto name

```bash
backuptools -R <resource> create
```

With specific name

```bash
backuptools -R <resource> create <version>
```

## Extract local version

```bash
backuptools -R <resource> extract <version>
```

## Push version

Push one local version to remote

```bash
backuptools -R <resource> push <version>
```

Push all local versions to remote

```bash
backuptools -R <resource> push --all
```

## Pull version

Pull one remote version to remote

```bash
backuptools -R <resource> pull <version>
```

Pull all remote versions to local

```bash
backuptools -R <resource> pull --all
```

## Sync versions

Upload all local versions to remote and download all remote versions to local

```bash
backuptools -R <resource> sync
```

## Remove version

Remove one version on local and remote

```bash
backuptools -R <resource> rm <version>
```

Remove one version on local

```bash
backuptools -R <resource> rm <version> --local
```

Remove one version on remote

```bash
backuptools -R <resource> rm <version> --remote
```

Remove all version on local and remote

```bash
backuptools -R <resource> rm --all
```

Remove all version on local

```bash
backuptools -R <resource> rm --all --local
```

Remove all version on remote

```bash
backuptools -R <resource> rm --all --remote
```

# Development

## Prerequisites

```bash
pipenv install
```

## Test

1. Create Google Drive Service account and download json key

2. Copy to file to path **credentials/credentials.json**

3. Create file `test/local_config.py` with content:

```python
ROOT_ID = "1rbi0gr7yMAFKqEgx-pBp6kKJx1Z4Tcgm"
CREDENTIALS_PATH = 'credentials/credentials.json'

```

4. Test command line

```
./test.sh
```
