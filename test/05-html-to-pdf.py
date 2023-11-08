import pdfkit


fn_html = '../output-html/230328 TEE.html'
fn_pdf = 'my.pdf'
pdfkit.from_file(fn_html, fn_pdf)