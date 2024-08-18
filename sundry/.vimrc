set t_Co=16
set t_Co=256
syntax enable
" Status Line {  
        set laststatus=2                             " always show statusbar  
        set statusline=  
        set statusline+=%-10.3n\                     " buffer number  
        set statusline+=%f\                          " filename   
        set statusline+=%h%m%r%w                     " status flags  
        set statusline+=\[%{strlen(&ft)?&ft:'none'}] " file type  
        set statusline+=%=                           " right align remainder  
        set statusline+=0x%-8B                       " character value  
        set statusline+=%-14(%l,%c%V%)               " line, character  
        set statusline+=%<%P                         " file position  
"} 
" colorscheme dimgreens
" colorscheme bluegreen
" colorscheme foobar
" colorscheme brookstream
" colorscheme baycomb
" colorscheme solarized
" colorscheme ir_black
" colorscheme wombat256mod
" colorscheme pyte
" colorscheme railscasts
" colorscheme intellij
" colorscheme mickeysoft
" colorscheme summerfruit256
" colorscheme github
" colorscheme default
"colorscheme foobar
if &diff
    syntax off
    " colorscheme foobar
endif


set hlsearch        " highligh search patter
set ai
set nu
set tabstop=4       " tab character counts as 8 spaces
set softtabstop=4   " tab key should insert 4 spaces
set shiftwidth=4    " autoindent step should be 4 spaces
set expandtab       " tab key should generate space chars only
"set textwidth=80   " wrap lines at this size
"set tw=80          " wrap lines at this size
                    " use gq after visual selecting a block to wrap
set showmatch       " show matches on parens, brackets, etc
set ic              " Ignore case
"set foldmethod=marker
"let perl_fold=1 
"let perl_fold_blocks=1
set nowrapscan
set viminfo=%,'50,\"100,n~/.viminfo

"set diffopt+=iwhite     " don't igmore whitespace
"set diffopt-=iwhite      " ignore whitespace

highlight! link DiffText MatchParen
if &diff                             " only for diff mode/vimdiff
  set diffopt=filler,context:1000000 " filler is default and inserts empty lines for sync
  set diffopt+=iwhite
endif

" stop beeps
"set belloff=all       " works on mac, not on ubuntu
set noeb vb t_vb=      " works on both
set nomodeline
set encoding=utf-8

"set mouse=a
map <ScrollWheelDown> k
map <ScrollWheelUp> j
