if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

let s:pyscript = resolve('~/.vim/bundle/lsac/parse.py')
let s:pyscript_lua = resolve('~/.vim/bundle/lsac/parse_lua.py')
let s:pyscript_scala = resolve('~/.vim/bundle/lsac/parse_scala.py')

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

function! LsacCompleteLua()
    let s:wordUnderCursor = expand("<cword>")
    execute 'python import sys'
    execute 'python sys.argv = ["complete"]'
    execute 'pyfile ' . s:pyscript_lua
endfunction

function! LsacParseLua()
    execute 'python import sys'
    execute 'python sys.argv = ["parse"]'
    execute 'pyfile ' . s:pyscript_lua
endfunction

function! LsacCompleteScala()
    execute 'python import sys'
    execute 'python sys.argv = ["complete"]'
    execute 'pyfile ' . s:pyscript_scala
endfunction

function! LsacParseScala()
    execute 'python import sys'
    execute 'python sys.argv = ["parse"]'
    execute 'pyfile ' . s:pyscript_scala
endfunction
