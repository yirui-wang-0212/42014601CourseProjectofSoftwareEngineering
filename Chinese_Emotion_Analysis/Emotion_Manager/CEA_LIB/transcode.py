import codecs
import os

BLOCKSIZE = 1048576
FindPath = 'raw_data/3000/neg/'
FileNames = os.listdir(FindPath)
for file_name in FileNames:
    full_file_name = os.path.join(FindPath, file_name)
    if 'utf8' in full_file_name:
        break
    with codecs.open(full_file_name, 'r', 'GBK') as f:
        with codecs.open(full_file_name+ "_utf8", "w", "utf-8") as target_file:
            try:
                while True:
                    contents = f.read(BLOCKSIZE)
                    if not contents:
                        break
                    target_file.write(contents)
            except UnicodeDecodeError:
                print(full_file_name)