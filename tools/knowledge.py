#!/usr/bin/env python3
"""Offline lookup/search. Results may contain spoilers; AI must enforce run spoiler policy."""
import argparse,json
from common import lookup,records,dump,slug

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('category',choices=['characters','classes','weapons','items','skills','chapters','enemies']);p.add_argument('query');p.add_argument('--search',action='store_true');a=p.parse_args()
 try:dump([{'id':r['id'],'name':r['name'],'verification':r['verification']} for r in records(a.category) if slug(a.query) in slug(r['name'])] if a.search else lookup(a.category,a.query))
 except ValueError as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
