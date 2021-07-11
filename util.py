from multiprocessing.pool import ThreadPool
import argparse
import logging
import os
import shutil


logging.basicConfig(filename='logs.log',
                    filemode='w', 
                    format='%(asctime)s - %(levelname)s: %(message)s', 
                    datefmt='%m.%d.%Y %H:%M:%S', level=logging.DEBUG)

class MultiThread:
    def __init__(self, threads):
        self.pool = ThreadPool(threads)

    def copy_tree(self, src, dst):
        """ Copy files from source path to destination path"""
        for root, dirs, files in os.walk(src):
            dst_dir = root.replace(src, dst, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                self.copy(src_file, dst_dir)

    def copy(self, src, dst):
        """ Copy the file using shutil.copy2 """
        self.pool.starmap(shutil.copy2, [(src, dst)])

    def copy_file(self, src, dst, copy_function=None):
        """ Copy file by extension from source path to destination path"""
        for file in self.list_files_by_extension(src):
            if os.path.isfile(file):
                if copy_function:
                    try:
                        shutil.move(file, dst, copy_function)
                    except shutil.Error as e:
                        logging.error("Destination path '%s' already exists" % file)
                else:
                    self.copy(file, dst)

    def list_files_by_extension(self, _path):
        """Get a list of all files in a directory"""
        if os.path.isdir(os.path.basename(_path)):
            return os.listdir(_path)

        return [os.path.join(root, file) 
            for root, dirs, files in os.walk(os.path.dirname(_path))
            for file in files 
            if file.endswith(os.path.basename(_path))
        ]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', dest='operation', help='choice operation (copy or move)')
    parser.add_argument('--from', dest='_from', help='Сhoose the path "from"')
    parser.add_argument('--to', dest='_to', help='Сhoose the path "to"')
    parser.add_argument('--threads', dest='thread', type=int, default=1, help='Choose amount of threads')

    args = parser.parse_args()
    with MultiThread(threads=int(args.thread)) as pool:
        if args.operation == 'move':
            if os.path.isdir(args._from):
                shutil.move(args._from, args._to, copy_function=pool.copy)
            else:
                pool.copy_file_by_extension(args._from, args._to, copy_function=pool.copy)
        elif args.operation == 'copy':
            if os.path.isdir(args._from):
                pool.copy_tree(args._from, args._to)
            else:
                pool.copy_file_by_extension(args._from, args._to)
        else:
            logging.error(f'Invalid operation entered {args.operation}')


if __name__ == '__main__':
    main()