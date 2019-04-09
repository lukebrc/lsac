if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

let s:pyscript = resolve('~/.vim/bundle/lsac/parse.py')

function! LsacComplete()
    let s:wordUnderCursor = expand("<cword>")
    execute 'python import sys'
    execute 'python sys.argv = ["complete"]'
    "let s:currentLine = getline(".")
    execute 'pyfile ' . s:pyscript
endfunction

function! LsacParse()
    execute 'python import sys'
    execute 'python sys.argv = ["parse"]'
    execute 'pyfile ' . s:pyscript
endfunction
