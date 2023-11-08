import markdown

fn_html = 'my.html'




markdown_text = """
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1, Column 1 | Row 1, Column 2 | Row 1, Column 3 |
| Row 2, Column 1 | Row 2, Column 2 | Row 2, Column 3 |
"""

md_html = markdown.markdown(markdown_text, extensions=['tables'])


html = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Example</title>
    <style>
      table {
        border-collapse: collapse;
        border-spacing: 0;
      }

      th,
      td {
        border: 1px solid black;
        padding: 6px;
      }    
    </style>
  </head>
  <body>
    <!-- Markdown-generated HTML content here -->
    %s
  </body>
</html>
'''

html = html % (md_html)


f = open(fn_html, 'w')
f.write(html)
f.close()

