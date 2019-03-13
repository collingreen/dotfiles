#! /usr/bin/env python3

# TODO: interactive mode

import os
import subprocess
import sys

def get_repo_root():
    return subprocess.check_output('git rev-parse --show-toplevel', shell=True).strip()

def get_untracked_files(repo_root):
    untracked_files = []
    content = subprocess.check_output('git status --porcelain .', shell=True)
    for line in content.splitlines():
        if line.startswith('??'):
            # get the file path (after ?? ) - ?? local/path/to/file
            path = line[3:]

            # make absolute path by adding the repo root (so this can be called from anywhere)
            abs_path = os.path.join(repo_root, path)
            if os.path.isfile(abs_path):
                untracked_files.append(abs_path)

    return untracked_files

def show_help():
    print("""
y - yes delete this file
a - yes and delete all other files without asking
n - no do not delete this file
q - no and stop deleting files
? - show help
""")

def remove_file(path):
    os.unlink(path)

if __name__ == '__main__':
    repo_root = get_repo_root()
    untracked_files = get_untracked_files(repo_root)
    if len(untracked_files) > 0:
        print('Found {} untracked files (new directories ignored)'.format(len(untracked_files)))

        do_prompt = True
        while len(untracked_files) > 0:
            path = untracked_files[0]
            if do_prompt:
                print(' > {}'.format(path))
                choice = raw_input('Delete this file? [y/a/n/q/?]: ').lower().strip()
                if choice == '?':
                    show_help()
                elif choice == 'y':
                    remove_file(path)
                    untracked_files = untracked_files[1:]
                elif choice == 'a':
                    remove_file(path)
                    untracked_files = untracked_files[1:]
                    do_prompt = False
                elif choice == 'n':
                    untracked_files = untracked_files[1:]
                elif choice == 'q':
                    print('Aborting')
                    sys.exit(0)
                continue
            else:
                remove_file(path)
