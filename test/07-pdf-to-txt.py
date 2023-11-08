import os 
import PyPDF2

pdf_file = 'hkg18-402-180328091217.pdf'

output_file = '%s.txt' % pdf_file

# Open the PDF file in read-binary mode
with open(pdf_file, 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)

    # Initialize an empty string to store the extracted text
    extracted_text = ''

    # Iterate through the pages and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += 'Page %d\n\n' % (page_num+1)
        extracted_text += page.extract_text()
        extracted_text += '\n\n'

# Save the extracted text to a file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(extracted_text)