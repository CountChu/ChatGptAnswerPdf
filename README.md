# ChatGptAnswerPdf
The projects support python applications that help you convert your ChatGPT conversations from Markdown files into HTML and PDF files.

# Applications

## chat2md.py

The app converts conversations.json into Markdown files which are compatible to the Chrome plugin, [ChatGPT to Markdown](https://chatopenai.pro/chatgpt-to-markdown/).

The conversations.json is downloaded from Settings menu of ChatGPT website by clicking "Export data".
> ChatGPT > Settings & Beta > Data controls > Export data. 

## chatpdf.py

The app generates answers of ChatGPT and saves them in HTML and PDF files by running the tool chain: 
> answer.py, subl_markdownPreview_save.py, and topdf.py. 

```
answer.py:                      chats(md), questions(yaml) ---> out-ans(md)
subl_markdownPreview_save.py:   out-ans(md) --> out-ans-html
topdf.py:                       out-ans-html ---> out-ans-pdf
```

The answers are extracted from chat files (\*.md) and organized by question set files (\*.yaml).

The chat files (\*.md) are converted by chat2md.py from conversations.json or  captured by the Chrome plugin [ChatGPT to Markdown](https://chatopenai.pro/chatgpt-to-markdown/).

## history.py

The app generates answers in Markdown files for each date. The answers come from all question set files answered by chat files or all chat files.

# Usages

List all question set files.
```
% python chatpdf.py list

Question Sets in the directory "questions":
    230327.OP-TEE.SP.yaml
    230327.OP-TEE.yaml
    230328.TEE.yaml
    230329.TrustZone.yaml
    230330.OP-TEE.Intel.yaml
    230330.OP-TEE.j721e.yaml
    230330.Questions.yaml
    230402.DRM.yaml
```

Update PDF files if your question set files are updated.
```
% python chatpdf.py update
```

Enforce to update (clean build) all PDF files for all question set files.
```
% python chatpdf.py build
```

Enforce to build the PDF files by a given question set file.
```
% python chatpdf.py build -f 230328.TEE.yaml
```

Convert conversations.json into Markdown files for each chat. The download-230414 is an example directory where conversations.json resides.
```
python chat2md.py -i download-230417 -o chats
```

Generate Markdown files that contain questions that come from all question set files answered by chat files. The Markdown files are for each date.
```
python history.py -q questions -c chats -o out-hist-qst
```

Generate Markdown files that contain the above description plus **"solo chats"**. The Markdown files are for each date.

**"solo chat"** means a chat is not related to a question in a question set file.
```
python history.py -q questions -c chats -o out-hist-mgt --merge
```

Generate Markdown files that contain all chat files for each date.
```
python history.py -c chats -o out-hist-cht
```

# File Structure
```
[ChatGptAnswerPdf]
    [user-Alice]        ---- A working directory of the user, Alice.
        [chats]         ---- A directory that contains MD chat files 
                             converted by chat2md.py from conversations.json.  
        [chats-manual]  ---- A directory that contains MD chat files 
                             saved by the Chrome plugin, 
                             "ChatGPT to Markdown".                          
        [download]      ---- A directory where conversations.json resides.                      
        [questions]     ---- A directory that contains question set files.
        [out-ans]       ---- An output directory that contains MD files 
                             generated by answer.py
        [out-ans-html]  ---- An output directory that contains HTML files
                             converted by subl_markdownPreview_save.py 
                             from out-ans.
        [out-ans-pdf]   ---- An output directory that contains PDF files
                             converted by topdf.py from out-ans-html.
        [out-hist-mrg]  ---- An output directory that contains MD files 
                             generated by history.py in the option, --merge
        [out-hist-mrg-txt]  
                        ---- An output directory that contains TEXT files
                             generated by history.py in the option, --merge
        [out-hist-mrg-html]  
                        ---- An output directory that contains HTML files
                             converted by subl_markdownPreview_save.py 
                             from out-hist-mrg. 
        [out-hist-mrg-pdf]  
                        ---- An output directory that contains PDF files
                             converted by topdf.py from out-hist-mrg-html             
    [core]          ---- A Python package that contains common functions 
                         called by apps.
    chatpdf.py      ---- A main Python app that consumes answer.py, tohtml.py
                         and topdf.py to generate PDF files 
                         in the output-pdf directory. 
    chat2md.py      ---- A main Python app that converted conversations.json 
                         into Markdown files.
    history.py      ---- A main Python app that generate answers in MD files
                         for each date.
    answer.py       ---- A Python app that generate MD files.
    subl_markdownPreview_save.py  
                    ---- The app converts MD files into HTML files 
                         with the Sublime plug-in, MarkdownPreview.
    topdf.py        ---- A Python app that converts HTML files into pdf files.
```


