"""Game assets and where they are located"""

from os import path
from .aim_assist_dict import aim_assist_asset_dict as asset_dict

# The absolute path of the current file's directory.
main_dir = path.split(path.abspath(__file__))[0]
data_dir = path.join(main_dir, "data")


def get(key):
    # Throws a KeyError if key doesn't exist
    try:
        value = asset_dict[key]
    except KeyError:
        print(
            f'The asset key {key} is unknown and a KeyError exception was raised.'
        )
        raise
    value = path.join(data_dir, value)
    # Make sure path exists
    assert path.exists(value)
    return value
