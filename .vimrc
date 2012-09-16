syntax on

setlocal foldlevel=1

set sw=4
set ts=4
set number
filetype indent on
filetype plugin indent on
autocmd FileType python setlocal et sta sw=4 sts=4

autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascrīpt set omnifunc=javascrīptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
