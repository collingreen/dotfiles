Dotfiles
--------

A simple collection of dotfiles and other helper files mostly
about vim. Started from https://github.com/jwilm/dotfiles, which
is far more complete.

Clone into a folder where you want to keep your files
(~.dotfiles perhaps?), then follow the install instructions
below to update all the submodules and link all the dotfiles
into your home directory. Everything will be contained in this
folder -- any updates here will be reflected in your settings.

Uninstalling is as simple as unlinking the various files in your
home directory (`unlink ~/.vimrc`, `unlink ~/.vim`, and
`unlink ~/.gitconfig` will get you a long way).


# Installation
- Go take my name and email out of the gitconfig
- `python install.py`


# Highlights
- Vim
 - fugitive
 - pathogen
 - ctrl p
 - highlight whitespace
 - long undo
 - swapfiles in a different location
 - syntax highlighting with syntastic
 - code folding
 - sane backspace functionality
 - 80 line highlighting
 - tab completion

- Git
 - those fantastic `lg` commands that show git timelines
