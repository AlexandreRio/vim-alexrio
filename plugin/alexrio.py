# -*- coding: utf-8 -*-

import HTMLParser
import json
import re
import textwrap
import urllib2
import vim
import webbrowser


API_URL = "http://alexrio.fr"

def bwrite(s):
  b = vim.current.buffer
  # Never write more than two blank lines in a row
  #if not s.strip() and not b[-1].strip() and not b[-2].strip():
  #  return

  # Vim buffer.append() cannot accept unicode type,
  # must first encode to UTF-8 string
  if isinstance(s, unicode):
    s = s.encode('utf-8', errors='replace')

  # Code block markers for syntax highlighting
  if s and s[-1] == unichr(160).encode('utf-8'):
    b[-1] = s
    return

  if not b[0]:
    b[0] = s
  else:
    b.append(s)


def alexrio():
  vim.command("edit .alexrio")
  vim.command("setlocal noswapfile")
  vim.command("setlocal buftype=nofile")

  bwrite("┌─────────────────────────────────────────┐")
  bwrite("│    Alexandre Rio – http://alexrio.fr    │")
  bwrite("└─────────────────────────────────────────┘")
  bwrite("")

  try:
    news1 = json.loads(urllib2.urlopen(API_URL+"/feed.json", timeout=5).read())
  except urllib2.HTTPError, e:
    print "alexrio.vim Error: %s" % str(e)
    return
  except:
    print "alexrio.vim Error: HTTP Request Timeout"
    return

  for i, item in enumerate(news1):
    if 'title' not in item:
      continue

    line = "%s%d. %s [%s]"
    line %= (" " if i+1 < 10 else "", i+1, item['title'], item['url'])
    bwrite(line)
    line = "%sposted on %s [%s]"
    line %= (" "*4, item['date'], item['url'])
    bwrite(line)
    bwrite("")


def alexrio_news_link(external=False):
  line = vim.current.line

  m = re.search(r"\[(.*)\]$", line)
  if m:
    id = m.group(1)
    if external:
      browser = webbrowser.get()
      browser.open("http://alexrio.fr"+id)
      return
    try:
      item = json.loads(urllib2.urlopen(API_URL+"/feed.json", timeout=5).read())
    except urllib2.HTTPError, e:
      print "alexrio.vim Error: %s" % str(e)
      return
    except:
      print "alexrio.vim Error: HTTP Request Timeout"
      return
    vim.command("edit .alexrio")
    item.index
    for index, value in enumerate(item):
      if value['url'] == id:
        bwrite(value['title'])
        bwrite("")
        print_content(value['content'])
        return
    return

html = HTMLParser.HTMLParser()

def print_content(content):
    for p in content.split("<p>"):
        if not p:
            continue
        p = html.unescape(p)

        # Convert <a href="http://url/">Text</a> tags
        # to markdown equivalent: (Text)[http://url/]
        s = p.find("a>")
        while s > 0:
            s += 2
            section = p[:s]
            m = re.search(r"<a.*href=[\"\']([^\"\']*)[\"\'].*>(.*)</a>",
                          section)
            # Do not bother with anchor text if it is same as href url
            if m.group(1)[:20] == m.group(2)[:20]:
                p = p.replace(m.group(0), "[%s]" % m.group(1))
            else:
                p = p.replace(m.group(0),
                              "(%s)[%s]" % (m.group(2), m.group(1)))
            s = p.find("a>")

        contents = textwrap.wrap(re.sub('<[^<]+?>', '', p), width=80)
        for line in contents:
            if line.strip():
                bwrite(line)
        if contents and line.strip():
            bwrite("")
