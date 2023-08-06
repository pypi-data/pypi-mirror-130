#!/usr/bin/python3

import sys
import os
import re
import argparse
import json
import traceback
import configparser
import pymysql
import yaml
from collections import defaultdict

def repl_main():
    parser = argparse.ArgumentParser(description="yet another mysql client CLI tool/shell")
    parser.add_argument( "-s", "--source", dest="source", default=None, help="caculate replication topo from",)
    parser.add_argument( "-P", "--pool", dest="pool", default=None, help="full server list.",)
    parser.add_argument( "--detail", dest="detail", action="store_true", default=False, help="show detail",)
    parser.add_argument( "--noshift", dest="noshift", action="store_true", default=False, help="don't shift children when showing detail",)
    parser.add_argument( "-X", "--debug", dest="debug", action="store_true", default=False, help="debug mode",)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.my.cnf"))
    config = config._sections

    dftuser   = config.get('client',dict()).get('user',None)
    dftpasswd = config.get('client',dict()).get('password',None)
    dfthost   = config.get('client',dict()).get('host',None)
    dftport   = config.get('client',dict()).get('port',None)
    dftdb     = config.get('client',dict()).get('database',None)

    dbpool = dict()

    def get_repl(host) :
        user   = config.get(host,dict()).get('user',None) if args.source in config  else dftuser
        passwd = config.get(host,dict()).get('password',None) if args.source in config else dftpasswd
        port   = (config.get(host,dict()).get('port',3306) if args.source in config else dftport) or 3306
        db     = (config.get(host,dict()).get('db',None) if args.source in config else dftdb) or "mysql"
        if args.debug :
            conn_paras = {"user":user,"password":passwd,"host":host,"port":port,"database":db}
            print("# conn_paras : ", json.dumps(conn_paras))
        repl = dict()
        dbconn = pymysql.connect(host=host,user=user,password=passwd,database=db)
        with dbconn :
            with dbconn.cursor() as cursor :
                downstream_sql = "select * from performance_schema.threads where 1=1 and processlist_command = 'Binlog Dump GTID'"
                cursor.execute(downstream_sql)
                columns = [ col[0] for col in cursor.description]
                rows = cursor.fetchall()
                for r in rows :
                    if "downstreams" not in repl :
                        repl['downstreams'] = list()
                    repl['downstreams'].append(dict(zip(columns,r)))
                upstream_sql = "select c.*, s.thread_id, s.service_state from performance_schema.replication_connection_configuration c, performance_schema.replication_connection_status s where 1=1"
                cursor.execute(upstream_sql)
                columns = [ col[0] for col in cursor.description]
                rows = cursor.fetchall()
                for r in rows :
                    if "upstreams" not in repl :
                        repl['upstreams'] = list()
                    repl['upstreams'].append(dict(zip(columns,r)))
        return repl

    if args.source :
        dbpool[args.source] = get_repl(args.source)
    if args.pool:
        for host in [src for src in args.pool.split(",") if src ] :
            if args.source and args.source == host :
                continue
            dbpool[host] = get_repl(host)

    if args.debug :
        print(json.dumps(dbpool,indent=2))

    heads = list()
    if args.source :
        heads.append(args.source)
    else :
        heads += [ host for host, repl in dbpool.items() if "upstreams" not in repl ]
    if args.debug :
        print("# heads = ", json.dumps(heads))

    details = list()

    visited=set()
    def tree_print(head, shft="", running=True) :
        if head is None :
            return
        if shft :
            if running :
                print(shft+"---> "+head)
            else :
                print(shft+"xx-> "+head)
        else :
            print(head)
        details.append((head,shft))
        if head in visited :
            return
        visited.add(head)
        for h,repl in dbpool.items() :
            if "upstreams" not in repl :
                continue
            ischild = False
            running = False
            for r in repl["upstreams"] :
                if r["HOST"] != head :
                    continue
                ischild = True
                running = r['service_state'] == "ON"
                break
            if not ischild :
                continue
            tree_print(h,shft+"    ",running)

    for h in heads :
        tree_print(h)
                
    if args.detail :
        for h, shft in details :
            if args.noshift :
                print(yaml.safe_dump({h:dbpool[h]}))
            else :
                print("\n".join([shft*2+ln for ln in yaml.safe_dump({h:dbpool[h]}).splitlines()]))

if __name__ == "__main__" :
    repl_main()


