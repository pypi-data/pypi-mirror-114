''' Author: yanyuxiangtoday '''

import os
import numpy as np

def save_file(dump_path: str,
              content: str or np.array,
              keep_ori: bool):
    if not keep_ori and os.path.exists(dump_path):
        os.system(f'rm {dump_path}')

    if dump_path[-4:] != '.txt' and dump_path[-4:] != '.csv':
        raise Exception('wrong type to save')

    if isinstance(content, str):
        with open(dump_path, 'a') as dump_file:
            dump_file.write(content)
    elif isinstance(content, type(np.array(0.0))):
            np.savetxt(dump_path, content, fmt='%.5f', delimiter=',')
    else:
        raise Exception('wrong content type')

    return

