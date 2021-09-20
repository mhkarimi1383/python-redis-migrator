#!/usr/bin/env python3

import argparse
import redis
from tqdm import tqdm
from multiprocessing.pool import ThreadPool as Pool

def connect_redis(conn_dict, password=None, connection_pool=8):
    conn = redis.StrictRedis(host=conn_dict['host'],
                             port=conn_dict['port'],
                             db=conn_dict['db'],
                             password=password
                             connection_pool=connection_pool)
    return conn


def conn_string_type(string):
    format = '<host>:<port>/<db>'
    try:
        host, portdb = string.split(':')
        port, db = portdb.split('/')
        db = int(db)
    except ValueError:
        raise argparse.ArgumentTypeError('incorrect format, should be: %s' % format)
    return {'host': host,
            'port': port,
            'db': db}

def migrate_key(src, dst, key):
    ttl = src.ttl(key)
    # we handle TTL command returning -1 (no expire) or -2 (no key)
    if ttl < 0:
        ttl = 0
    value = src.dump(key)
    try:
        dst.restore(key, ttl * 1000, value, replace=True)
    except redis.exceptions.ResponseError:
        print ("Failed to restore key: %s" % key)
        pass

def migrate_redis(source, destination, pool_size=8, source_password=None, destination_password=None, connections=8):
    src = connect_redis(source, source_password, connections)
    dst = connect_redis(destination, destination_password, connections)
    pool = Pool(pool_size)
    for key in tqdm(src.keys('*')):
        pool.apply_async(migrate_key, (src, dst, key,))

    pool.close()
    pool.join()

    return


def run():
    parser = argparse.ArgumentParser(description='''
    A simple & multithreaded Redis Migrator in python.
    Note -> Connection strings should be in this format: <host>:<port>/<db>
    Critical Note -> You Need memory a little bit highter than data that you want to transfer (You Will not lose your data)
    ''')
    parser.add_argument('source', type=conn_string_type, help='Connection string for Source Database')
    parser.add_argument('destination', type=conn_string_type, help='Connection string for Destination Database')
    parser.add_argument('--pool', '-p', type=int, default=8, help='How many threads to open? Default: 8')
    parser.add_argument('--source-password', '-s', type=str, default=None, help='Password to connect to source database')
    parser.add_argument('--destination-password', '-d', type=str, default=None, help='Password to connect to destination database')
    parser.add_argument('--connections', '-c', type=int, default=8, help='Number of connection to use in connection pool for each database')

    options = parser.parse_args()
    migrate_redis(options.source, options.destination, options.pool_size, options.source_password, options.destination_password, options.connections)

if __name__ == '__main__':
    run()
