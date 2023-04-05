# ChatGptAnswerPdf
Support python applications that help you generate PDF files from Markdown files of ChatGPT.

The project supports a set of python applications that help you transform Markdown files catched by the Chrome plugin [ChatGPT to Markdown](https://chatopenai.pro/chatgpt-to-markdown/) into PDF files filtered by your question set files in TXT project-specific format.

# Usage

Display all your question set files.
```
python chatpdf.py list  
```

Refresh PDF files if your question set files are updated.
```
python chatpdf.py refresh
```

Enforce to build the PDF files by a given question set file.
```
python chatpdf.py build -f 230328.TEE.txt
```
