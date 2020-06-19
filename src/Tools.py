def clear_folder(path):
    import os
    import shutil
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Error: %s' % e)


def write_file(data, path):
    import json
    with open(path, 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, sort_keys=True))