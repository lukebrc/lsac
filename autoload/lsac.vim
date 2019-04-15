if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! LsacComplete()
    let s:parser = resolve('~/.vim/bundle/lsac/parser.py')
    if &filetype == "scala"
        call ExecLsacFunction(s:parser, 'scala', 'complete')
    elseif &filetype == "python"
        call ExecLsacFunction(s:parser, 'python', 'complete')
    elseif &filetype == "lua"
        call ExecLsacFunction(s:parser, 'lua', 'complete')
    else
        echo "Unknown type: " &filetype
    endif
endfunction

function! LsacParse()
    let s:parser = resolve('~/.vim/bundle/lsac/parser.py')
    if &filetype == "scala"
        call ExecLsacFunction(s:parser, 'scala', 'parse')
    elseif &filetype == "python"
        call ExecLsacFunction(s:parser, 'python', 'parse')
    elseif &filetype == "lua"
        call ExecLsacFunction(s:parser, 'lua', 'parse')
    else
        echo "Unknown type: " &filetype
    endif
endfunction

function! ExecLsacFunction(script_path, ftype, lsac_fun)
    "let s:wordUnderCursor = expand("<cword>")
    let s:currentLine = getline(".")
    let s:currentPath = expand('%')
    let s:pyPluginPath = expand('~/.vim/bundle/lsac')
    execute 'python import sys'
    execute 'python sys.argv = ["' . a:ftype . '", "' . a:lsac_fun . '"]'
    execute 'pyfile ' . a:script_path
endfunction

