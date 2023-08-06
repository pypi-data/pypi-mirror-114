# qronos-client
Python client for QRonos

## Installation

This package can be installed via pip:

```
pip install qronos-client
```

## Example Usage

```python
from qronos import QRonosClient

# Create client and login
qronos = QRonosClient(host='dev.qronos.xyz')
token, expiry = qronos.login(username='Quentin', password='Rogers')

# Alternatively if you already have a token
qronos = QRonosClient(host='dev.qronos.xyz', token='ABCDEFGHIJKLMN')

# Import Tracker (Item) Data
job_id = qronos.tracker_import(
    tracker_id=24,
    unique_columns=["Part Number", "Weight"], 
    can_add_item=True,
    can_delete_item=False,
    data=[{"Part Number": "A1", "Weight": 5}, {"Part Number": "A2", "Weight": 8}],
)

# Import Stage Data
job_id = qronos.stage_import(
    stage_id=2,
    data=[{"Part Number": "A1", "leadtime": 5}, {"Part Number": "A2", "actual": "2020-10-26"}],
)

# Delete Items
job_id = qronos.delete_items(
    tracker_id=2, 
    data=["A", "B"],
)

# Check Status of an Import
status = qronos.import_status(job_id=job_id)

# Logout
qronos.logout(all_tokens=True)
```

## Testing

Speak with a QRonos Demo Site Admin for credentials in order to run the tests.
