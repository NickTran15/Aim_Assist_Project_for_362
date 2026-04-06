"DONE"

"Logic to find game assets in asset dictionary"

from os import path
from .aim_assist_dict import aim_assist_asset_dict as asset_dict

main_dir = path.split(path.abspath(__file__))[0]
data_dir = path.join(main_dir, "data")

def get(key):

    value = asset_dict[key]
    value = path.join(data_dir, value)
    assert path.exists(value)
    
