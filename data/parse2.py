"""Parses Amazon product metadata found at http://snap.stanford.edu/data/amazon/productGraph/metadata.json.gz"""

import sys, csv
import ast

def usage():
    print """
USAGE: python parse.py metadata.json
"""
    sys.exit(0)

def main(argv):
    if len(argv) < 2:
        usage()
    filename = sys.argv[1]
    out = csv.writer(open("products.csv","w"))
    with open(filename, 'rb') as f:
        products = []
        count, good, bad = 0, 0, 0
        loads=ast.literal_eval
        for line in f:
            count += 1
            if not (count % 100000):
                print "count:", count, "good:", good, ", bad:", bad
            try:
                product = loads(line.rstrip())
                title, brand, categories, description = product.get('title',''), product.get('brand',''), product.get('categories',''), product.get('description','')
                categories = ' / '.join([item for sublist in categories for item in sublist])
                out.writerow([title, brand, description, categories])
                good += 1
            except Exception as e:
                print line
                print e
                bad += 1
        print "good:", good, ", bad:", bad

if __name__ == "__main__":
    main(sys.argv)
