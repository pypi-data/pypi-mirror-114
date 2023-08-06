PySIO allows reading of SLAC's Serial Input Output format inside Python.

Only the reading of record headers are currently supported. The block payload is stored as (compressed) raw data.

## Example
To iterate over all records in a file and print the record name:

```python
import sio

fileName='muonGun_sim_MuColl_v1.slcio'
for record in sio.read_sio(fileName):
    print(record.name)
```



