"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if exists("b:current_syntax")
  finish
endif



" Make sure `Ignore` highlight group is hidden
" Some colorschemes do not hide the `Ignore` group (ex. Solarized)
" An exception will be raised here if ctermfg=NONE which is sometimes set
" when using a transparent terminal so we wrap these commands in try/catch
try
    if has('gui_running')
        highlight Ignore guifg=bg
    else
        highlight Ignore ctermfg=bg
    endif
catch
endtry

" Remove emphesis from all components of main page item except title
syn match Comment /^\s*[0-9]\{1,2}\.\s/
syn match Comment /\s(\S\+\.\S\+)/
syn match Comment /^\s\{4}.*posted on [0-9]\{2} .\{3} [0-9]\{4}/

" Hide page url at end of main page lines
syn match Ignore /\s\[.*.html\]$/

" Highlight links
syn region Constant start="\[http" end="\]"

" Highlight code blocks
syn region Statement start="^\s+ " end="^\s "

" Highlight header orange
syn match Title /^┌.*$/
syn match Title /^│.*$/
syn match Title /^└.*$/
highlight Title ctermfg=69 guifg=#21759B


let b:current_syntax = "alexrio"
set listchars=
