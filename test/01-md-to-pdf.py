import markdown2pdf3
import pdb
br = pdb.set_trace

fn_md = '../output/230327 OP-TEE.md'
fn_pdf = 'my2.pdf'

markdown2pdf3.convert_markdown_to_pdf(fn_md, 'my.pdf')
markdown2pdf3.convert_markdown_to_pdf(fn_md, 'my2.pdf', pdf_engine="pdflatex")
