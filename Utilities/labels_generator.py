import argparse


OUTPUT_PATH = '/Users/victorhe/Pictures/tileDataSet/%s.txt'

ap = argparse.ArgumentParser()
ap.add_argument('-c', '--classes', required=True, type=int,
                help='the number of distinct classes')
ap.add_argument('-i', '--instances', required=True, type=int,
                help='the number of instances per classes')
ap.add_argument('-n', '--name', default='labels',
                help='name of the labels file')
args = vars(ap.parse_args())

with open(OUTPUT_PATH % args['name'], "w") as text_file:
    for i in range(args['classes']):
        s = (str(i) + ' ') * args['instances']
        text_file.write(s)
