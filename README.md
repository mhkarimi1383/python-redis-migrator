# Python Redis Migrator
Simple multithreaded redis migrator using python
## How to run
1. install dependencies 
```bash
$ sudo pip3 install -r requirments.txt
```
2. run it
```bash
$ ./migrate.py -h
  usage: redis-1.py [-h] [--pool POOL] source destination

  A simple & multithreaded Redis Migrator in python.
  Note -> Connection strings should be in this format: <host>:<port>/<db>
  Critical Note -> You Need memory a little bit highter than data that you want to transfer (You Will not lose your data)

  positional arguments:
    source                Connection string for Source Database
    destination           Connection string for Destination Database

  optional arguments:
    -h, --help            show this help message and exit
    --pool POOL, -p POOL  How many threads to open? Default: 8
```

## TODO
- [ ] Add web GUI
- [ ] Add support for authentication
