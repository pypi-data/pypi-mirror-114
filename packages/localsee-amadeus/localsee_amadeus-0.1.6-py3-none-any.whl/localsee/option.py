import argparse

parser = argparse.ArgumentParser(description='Local Shower')

parser.add_argument('--path', type=str, default='.',
                    help='image path')
# Hardware specifications
parser.add_argument('--select_area', type=int, nargs='+', default=[200, 200, 60, 60],
                    help='select_area')
parser.add_argument('--show_area', type=int, nargs='+', default=[0, 0],
                    help='show_area')
parser.add_argument('--scale', type=int, default=3,
                    help='scale')
parser.add_argument('--border_size', type=int, default=2,
                    help='border_size')
parser.add_argument('--border_color', type=int, nargs='+', default=[255, 0, 0],
                    help='border_color')
args = parser.parse_args()
