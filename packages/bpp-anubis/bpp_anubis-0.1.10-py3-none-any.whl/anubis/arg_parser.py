import argparse


def parse_arguments():
    """
    Parses commandline arguments
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser('Running in parallel mode')

    # parallelism
    parser.add_argument('--processes', '-p',   required=True, type=int,  help='Maximum number of processes.', default=1)

    # total results/output
    parser.add_argument('--output_dir', '-of', required=True, type=str,  help='path to temporary output file', default='output')
    parser.add_argument('--zip_output', '-zo', help='toggle for zipping output', action='store_true')
    parser.add_argument('--save_output', '-so', help='toggle for removing output', action='store_true', default=False)

    # direct behave arguments (every bpp behave project requires these
    parser.add_argument('--env',       '-e',  required=True, type=str,  help='Environment to use for test run(s)', default=[], nargs='+')
    parser.add_argument('--res',       '-r',  required=True, type=str,  help='File path for aggregate results')
    parser.add_argument('--dir',       '-d',  required=True, type=str,  help='Path to a behave-like directory')
    parser.add_argument('--headless',  '-hd', help='toggle for headless browser', action='store_true')
    parser.add_argument('--browser',   '-b',  type=str,  help='Browser to use')
    parser.add_argument('--itags',     '-it', type=str,  help='Please specify behave tags to run', nargs='+')
    parser.add_argument('--etags',     '-et', type=str,  help='Please specify behave tags to exclude', default=[], nargs='+')
    parser.add_argument('--retry',     '-rt', type=int,  help='Max number of tries')

    # accounts arguments
    parser.add_argument('--account_file',    '-a',  required=True, type=str,  help='path to accounts ini file')
    parser.add_argument('--account_section', '-s',  required=True, type=str,  help='path to accounts ini file')

    # arbitrary project specific args (very breakable)
    parser.add_argument('--project_specific', nargs='+')
    return parser.parse_args()
