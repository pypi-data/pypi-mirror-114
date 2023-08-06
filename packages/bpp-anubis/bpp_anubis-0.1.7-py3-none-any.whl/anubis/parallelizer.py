import os
from subprocess import call
from .arg_parser import parse_arguments


def command_generator(account_feature_groups: list) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param account_feature_groups:
    :return:
    """
    # get arguments
    args = parse_arguments()

    # get data for constructing behave command
    process_name = account_feature_groups[0][0]
    account = account_feature_groups[0][1].split()
    feature_set = account_feature_groups[1]

    # construct the behave command
    results_json = None
    commands = []
    for env in args.env:
        optional_retry = f'-D retry="{args.retry}" ' if args.retry else ''
        optional_browser = f'-D browser="{args.browser}" -D headless="{args.headless}" ' if args.browser else ''
        tags = f'--tags="{" and ".join(args.itags)} and ({" or ".join(feature_set)}){f"".join(" and not {}".format(t) for t in args.etags)}" '

        results_json = f'{args.output_dir}/{env}_process_{process_name}.json'
        results_html = f'{args.output_dir}/{env}_process_{process_name}.html'

        project_specific_args = (' '.join([f"-D {arg}" for arg in args.project_specific]) if args.project_specific else ' ') + " "

        cmd = (
                f'behave '
                f'-D parallel="True" ' +             # parallel
                f'-D env="{env}" ' +                    # environment
                optional_retry +
                optional_browser +                      # browser (basically always chrome)
                f'-D user="{account[0]}" ' +            # account user name
                f'-D pass="{account[1]}" ' +            # account password
                tags +                                  # tags (include and exclude)
                project_specific_args +
                f'-f json.pretty -o {results_json} ' +  # formatter for results
                f'-f html -o {results_html} ' +         # formatter for html results
                args.dir
        )
        commands.append(cmd)

    # run the command(s)
    for command in commands:
        # print(f'\t- Process <{process_name}> running ...')
        print(command)
        r = call(command, shell=True)

    return results_json
