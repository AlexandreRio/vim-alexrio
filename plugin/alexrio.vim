"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if !has('python')
    echo "HackerNews.vim Error: Requires Vim compiled with +python"
    finish
endif


" Filetype plugins and syntax highlighting should be enabled
filetype plugin on
syntax on


" Import Python code
execute "python import sys"
execute "python sys.path.append(r'" . expand("<sfile>:p:h") . "')"
execute "python from alexrio import alexrio, alexrio_news_link"


command! Alexrio python alexrio()


au! BufRead,BufNewFile *.alexrio set filetype=alexrio
