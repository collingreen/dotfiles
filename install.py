#!/usr/bin/python

import os, subprocess

HERE = os.path.abspath(os.path.dirname(__file__))

def link_to_home_dir(path, link_name):
    try:
        os.symlink(
            os.path.join(HERE, path),
            os.path.join(
                os.path.expanduser("~"),
                link_name
            )
        )
    except OSError:
        pass

def link_files(paths):
    for source, link_name in paths:
        link_to_home_dir(source, link_name)

def update_submodules():
    subprocess.call("git submodule update --init --recursive", shell=True)

def install_git():
    link_to_home_dir("git/gitconfig", ".gitconfig")

def install_vim():
    link_files([
        ("vim/vimrc", ".vimrc"),
        ("vim/vim", ".vim")
    ])


if __name__ == "__main__":
    update_submodules()
    install_git()
    install_vim()
