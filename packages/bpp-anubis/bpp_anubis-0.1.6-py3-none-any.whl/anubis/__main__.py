# __main__.py
import os
import sys
import multiprocessing
from datetime import datetime
from multiprocessing import Pool
import shutil


# custom
from . import account_splitter
from . import feature_splitter
from . import arg_parser
from .parallelizer import command_generator
from . import results


def main():
    # parse arguments
    arguments = arg_parser.parse_arguments()

    # create a temp dir that will contain results and be exported
    output_path = os.path.join('.', arguments.output_dir)
    if os.path.isdir(output_path):
        os.rmdir(output_path)
    os.mkdir(output_path)

    # set up the multiple processes
    # todo - set spawn method based on os (macos -> fork; others -> default)
    multiprocessing.set_start_method('fork')
    pool = Pool(arguments.processes)

    # get account data available for parallel runs
    print('--- Parsing accounts')
    print(f'\tfile:          <{arguments.account_file}>')
    print(f'\tsection:       <{arguments.account_section}>')
    accounts_data = account_splitter.get_accounts(
        arguments.processes,
        arguments.account_file,
        arguments.account_section
    )

    # split up the features and store as list
    print('--- Grouping features')
    print(f'\tfeature dir:   <{arguments.dir}>')
    print(f'\tincluded tags: <{",".join([t for t in arguments.itags])}>')
    print(f'\texcluded tags: <{",".join([t for t in arguments.etags])}>')
    account_feature_groups = feature_splitter.get_features(arguments, accounts_data)

    # run all the processes and save the locations of the result files
    print('--- Parallelizing')
    print(f'\tnum processes: <{len(account_feature_groups)}>')
    result_files = pool.map(command_generator, account_feature_groups)

    # input('ENTER to continue') # debug

    # recombine everything
    print('---RECOMBINING RESULTS')
    try:
        results.create_aggregate(
            files=result_files,
            aggregate_out_file=arguments.res
        )
    except Exception as e:
        print(e)

    # zip output if required
    if arguments.zip_output:
        results.zipper(output_path)

    # if arguments.sync_to:
    #     print(f'TODO: implement syncing to {arguments.sync_to}')
    #
    # if arguments.notify_to:
    #     print(f'TODO: implement notifying {arguments.notify_to}')

    if not arguments.save_output:
        os.rmdir(output_path)


if __name__ == '__main__':
    # run everything
    args = arg_parser.parse_arguments()
    start = datetime.now()
    main()
    end = datetime.now()

    # extremely basic summary
    print('\n========================================')
    print(f'Envs:     <{",".join(args.env)}>')
    print(f'Browser:  <{args.browser}>')
    print(f'Results:  <{args.res}>')
    print(f'Run Time: <{(end - start)}>')
    print('========================================')

    sys.exit(0)
