
if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! LsacComplete()
    if &filetype == "scala"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse_scala.py'), 'complete')
    elseif &filetype == "python"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse.py'), 'complete')
    elseif &filetype == "lua"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse_lua.py'), 'complete')
    else
        echo "Unknown type: " &filetype
    endif
endfunction

function! LsacParse()
    if &filetype == "scala"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse_scala.py'), 'parse')
    elseif &filetype == "python"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse.py'), 'parse')
    elseif &filetype == "lua"
        call ExecLsacFunction(resolve('~/.vim/bundle/lsac/parse_lua.py'), 'parse')
    else
        echo "Unknown type: " &filetype
    endif
endfunction

function! ExecLsacFunction(script_path, lsac_fun)
    "let s:wordUnderCursor = expand("<cword>")
    let s:currentLine = getline(".")
    execute 'python import sys'
    execute 'python sys.argv = ["' . a:lsac_fun . '"]'
    execute 'pyfile ' . a:script_path
endfunction

