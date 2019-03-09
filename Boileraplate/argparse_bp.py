import argparse

set_path_expression = '/Users/victorhe/Pictures/tileDataSet/%s'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())

set_param = args['set']