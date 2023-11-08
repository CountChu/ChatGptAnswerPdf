import markdown
import pdb
br = pdb.set_trace

fn_md = '../output/230327 OP-TEE.md'
fn_html = '../output/230327 OP-TEE.html'

f = open(fn_md)
md = f.read()
f.close()

html = markdown.markdown(md, extensions=['tables'])

f = open(fn_html, 'w')
f.write(html)
f.close()
