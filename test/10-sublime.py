import subprocess
import os

# Replace with the actual path to your Sublime Text executable
sublime_executable = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"

# Replace with the path to the Markdown file you want to preview
markdown_file = "/Users/visualge/Dropbox/CodeGitHubCount/ChatGptAnswerPdf/user-Count/out-hist-mrg/2023-08-24.md"

# Replace with the desired HTML output file path
html_output_file = "/Users/visualge/Dropbox/CodeGitHubCount/ChatGptAnswerPdf/user-Count/out-hist-mrg/2023-08-24.html"

# Open the Markdown file in Sublime Text
subprocess.run([sublime_executable, markdown_file])

# Delay to ensure the file is opened before previewing
input("Press Enter to continue...")

# Run the MarkdownPreview command to save the MD in HTML.

subprocess.run([sublime_executable, "--command", 'markdown_preview {"target":"save", "parser":"markdown"}'])

