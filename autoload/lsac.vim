if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

let s:pyscript = resolve('~/.vim/bundle/lsac/parse.py')

function! Append()
    let s:wordUnderCursor = expand("<cword>")
    let s:currentLine   = getline(".")
    execute 'pyfile ' . s:pyscript
endfunction

