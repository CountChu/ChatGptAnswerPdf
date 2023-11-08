import markdown
import pdb
br = pdb.set_trace

fn_md = '../output/230327 OP-TEE.md'
fn_html = '../output/230327 OP-TEE.html'

f = open(fn_md)
md = f.read()
f.close()

fn_css = '../github.css'
f = open(fn_css)
css = f.read()
f.close()

extensions = [
        #"markdown.extensions.smart_strong",
        "markdown.extensions.footnotes",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        "markdown.extensions.tables",
        "markdown.extensions.abbr",
        "markdown.extensions.md_in_html",
        #"pymdownx.extrarawhtml",
        
        "markdown.extensions.meta",
        "markdown.extensions.sane_lists",
        "markdown.extensions.smarty",
        "markdown.extensions.wikilinks",
        "markdown.extensions.admonition",

        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
	]

md_html = markdown.markdown(md, extensions=extensions)

html = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    %s
    </style>
    <title>Example</title>    
  </head>
  <body>
  	<article class="markdown-body">
    	<!-- Markdown-generated HTML content here -->
    	%s
  	</article>
  </body>
</html>
'''

html = html % (css, md_html)


f = open(fn_html, 'w')
f.write(html)
f.close()
