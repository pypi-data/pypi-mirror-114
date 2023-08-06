import argparse


def parse_arguments():
    """
    Parses commandline arguments
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser('Running in parallel mode')

    # misc
    parser.add_argument('--processes', '-p',  type=int,       help='Maximum number of processes.', default=1)
    parser.add_argument('--output_dir', '-of', type=str,       help='path to temporary output file', default='output')
    parser.add_argument('--zip_output', '-zo', help='boolean to zip run output', action='store_true')

    # direct behave arguments
    parser.add_argument('--env',       '-e',  type=str.lower, help='Environment to use for test run(s)', default=[], nargs='+')
    parser.add_argument('--course',    '-c',  type=str.lower, help='The course [mcat, lsat, etc]')
    parser.add_argument('--browser',   '-b',  type=str.lower, help='Browser to use')
    parser.add_argument('--headless',  '-hd', help='toggle for headless browser', action='store_true')
    parser.add_argument('--dir',       '-d',  type=str.lower, help='Path to a behave-like directory')
    parser.add_argument('--itags',     '-it', type=str,       help='Please specify behave tags to run', nargs='+')
    parser.add_argument('--etags',     '-et', type=str,       help='Please specify behave tags to exclude', default=[], nargs='+')
    parser.add_argument('--res',       '-r',  type=str,       help='File path for aggregate results', default='output/aggregate_results.json')
    parser.add_argument('--retry',     '-rt', type=int,       help='Number of tries')

    # accounts arguments
    parser.add_argument('--account_file',    '-a',  type=str,  help='path to accounts ini file')
    parser.add_argument('--account_section', '-s',  type=str,  help='path to accounts ini file')

    # syncing arguments
    parser.add_argument('--sync_to', '-st', type=str.lower, default=None)

    # notify arguments
    parser.add_argument('--notify_to', '-nt', type=str.lower, default=None)
    return parser.parse_args()
