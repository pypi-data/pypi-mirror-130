import json
import sys
from anubis.results_utils.results_utils_arguments import parse_arguments


def __create_aggregate(files: list, aggregate_out_file):
    aggregate = []
    for fp in files:
        with open(fp, 'r') as f:
            aggregate += json.load(f)
    with open(aggregate_out_file, 'w+') as f:
        f.write(json.dumps(aggregate))


def main():
    # parse arguments
    args = parse_arguments()
    __create_aggregate(args.files, args.output_file)


if __name__ == '__main__':
    # run everything
    main()
    sys.exit(0)
