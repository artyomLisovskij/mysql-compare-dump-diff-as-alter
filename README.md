# mysql-compare-dump-diff-as-alter
Compare two mysql dumps and output diffs of tables as CREATE TABLE, diff of fields as ALTER

# Dependencies
pip install parse

Tested on python3.6

# Usage
python mysql-diff.py dump1.sql dump2.sql diff.sql
