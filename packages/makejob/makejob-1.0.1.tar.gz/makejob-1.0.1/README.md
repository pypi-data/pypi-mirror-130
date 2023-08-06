# Generate job file quickly for SJM

## Installation
```python
python3 -m pip install makejob
```

## Example
```bash
cat demo.conf
# run_qc_1.sh 1G
# run_qc_2.sh 1G
# run_mapping.sh 2G run_qc_1.sh,run_qc_2.sh
# run_mutation.sh 3G run_mapping.sh 4

makejob demo.conf -o demo.job

# sjm demo.job
```
