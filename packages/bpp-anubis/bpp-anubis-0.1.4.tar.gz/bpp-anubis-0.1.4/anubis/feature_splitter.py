import os


def get_features(args, accounts) -> list:
    """
    Split the features as evenly as possible
    :param args:
    :param accounts:
    :return:
    """
    feature_data = [
        f'section.{f.split()[0]}' for f in
        os.listdir(os.path.join(args.dir)) if f.endswith('.feature')
    ]
    inc = -(-len(feature_data) // args.processes)  # weird, yucky
    features = [feature_data[i:i + inc] for i in range(0, len(feature_data), inc)]
    return list(zip(accounts, features))
