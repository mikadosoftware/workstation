sudo apt install vim=2:8.2.3995-1ubuntu2.15

git clone https://github.com/gmarik/Vundle.vim.git /home/pbrian/.vim/bundle/Vundle.vim


# NOTES
# sudo means the downloaded VUndle has root:root dir ownership and Vundle doe snot process. At end reassign ownerships. or not run as sudo - then struggles.

cat << EOF > /home/pbrian/.vimrc
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}

Plugin 'Syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'bling/vim-airline'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
EOF

cat << EOF >> /home/pbrian/.vimrc
" NERDTree Settings
" This should neatly append to end of .vimrc.
" it should alos make PageDOwn toggle my NERDTree on and off 
"nmap makes a normal mode key map in vim, and <PageDown> is obvious. Then it will run the escape mode instruction found followed by return
nmap <PageDown> :NERDTreeToggle<CR>

""""" WOrd wrapping
set number "(optional - will help to visually verify that it's working)
set textwidth=80
set wrapmargin=0
set formatoptions+=t
set linebreak " (optional - breaks by word rather than character)


EOF


POST_RUN_INSTRUCTIONS+="Start vim and run :PluginInstall \n"
