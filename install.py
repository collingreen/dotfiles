#!/usr/bin/python3

# TODO: replace with simple shell script
# TODO: idempotent install
# TODO: handle different linux flavors

import os, subprocess, logging

# logging.basicConfig(level=logging.DEBUG)

HERE = os.path.abspath(os.path.dirname(__file__))
PROFILE_HEADER = """
#### START AUTOMATICALLY GENERATED PROFILE CODE ####
"""
PROFILE_FOOTER = """
#### END AUTOMATICALLY GENERATED PROFILE CODE ####"""
PROFILE_CONTENT = """
# Do not edit anything inside this block. Your changes will be lost.
source ~/.custom_profile
"""


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

def install_one_offs():
    # TODO: this sucks - better way?

    # git diff so fancy - https://github.com/stevemao/diff-so-fancy
    subprocess.call("npm install -g diff-so-fancy", shell=True)
    subprocess.call(
        'git config --global core.pager "diff-so-fancy | less --tabs=1,5 -R"',
        shell=True
    )

    # httpie
    subprocess.call('pip install httpie', shell=True)

def install_profile():
    logging.info("Adding custom profile link to .profile")
    link_to_home_dir("custom_profile", ".custom_profile")

    # update .profile to source .custom_profile
    profile_path = os.path.join(os.path.expanduser('~'), '.profile')
    _update_profile(profile_path)

def _update_profile(profile_path):

    content = ''
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            content = f.read()

        # look for profile header and footer
        header_index = content.find(PROFILE_HEADER)
        footer_index = content.find(PROFILE_FOOTER)

        if header_index > -1 and footer_index > -1:
            logging.debug("Found existing header and footer")
            # rewrite internal section
            content = content[:header_index] + \
                PROFILE_HEADER + PROFILE_CONTENT + PROFILE_FOOTER + \
                content[footer_index + len(PROFILE_FOOTER):]
        elif header_index == -1 and footer_index == -1:
            logging.debug("Could not find header or footer")
            # add section to the end
            content = content + \
                    PROFILE_HEADER + PROFILE_CONTENT + PROFILE_FOOTER
        else:
            logging.warn("Failed to parse profile header and footer correctly")
    else:
        logging.debug(".profile not found - creating it")
        content = PROFILE_HEADER + PROFILE_CONTENT + PROFILE_FOOTER

    with open(profile_path, 'w') as f:
        f.write(content)


def install_misc_osx():
    subprocess.call("brew install gpg-agent", shell=True)
    subprocess.call("brew install ag", shell=True)
    subprocess.call("brew install diff-so-fancy", shell=True)
    subprocess.call("brew install tree", shell=True)

def install_misc_linux():
    subprocess.call("sudo apt-get update")
    subprocess.call("sudo apt-get install ripgrep")
    subprocess.call("sudo apt-get install tree")
    subprocess.call("sudo apt-get install zsh")
    subprocess.call('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)')

if __name__ == "__main__":
    update_submodules()
    install_git()
    install_vim()
    if os.name == 'darwin':
        install_misc_osx()
    elif os.name == 'posix':
        install_misc_linux()
    install_profile()
