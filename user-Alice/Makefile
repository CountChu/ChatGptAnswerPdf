#
# The below targets are for testing.
#

answer-1:
	python ../answer.py -q "questions-230402/230327.OP-TEE.SP.yaml" -c "chats-manual" -a "out-ans"

tohtml-1:
	python ../subl_markdownPreview_save.py -i out-ans -o out-ans-html

topdf-1:
	python ../topdf.py -i out-ans-html -o out-ans-pdf

#
# chat2md: download/conversations.json ---> chats(md)	
#

chat2md:
	python ../chat2md.py -i download-230421 -o chats

#
# chatpdf.py runs answer.py, subl_markdownPreview_save.py and topdf.py
#		answer.py: 					 	chats(md), questions(yaml) ---> out-ans(md)
#		subl_markdownPreview_save.py: 	out-ans(md) --> out-ans-html
#		topdf.py: 						out-ans-html ---> out-ans-pdf
# 

.PHONY: update
update:
	python ../chatpdf.py update

build:
	python ../chatpdf.py build

#
# Generate history of questions
#

hist-qst:
	python ../history.py -q questions -c chats -o out-hist-qst
	python ../subl_markdownPreview_save.py -i out-hist-qst -o out-hist-qst-html
	python ../topdf.py -i out-hist-qst-html -o out-hist-qst-pdf

#
# Generate history of chats
#

hist-cht:
	python ../history.py -c chats -o out-hist-cht
	python ../subl_markdownPreview_save.py -i out-hist-cht -o out-hist-cht-html
	python ../topdf.py -i out-hist-cht-html -o out-hist-cht-pdf

#
# Generate out-hist-mrg, out-hist-mrg-txt, out-hist-mrg-html
#
# history.py: chats(md), questions(yaml)  ---> out-hist-mrg(md), out-hist-mrg-txt
# subl_markdownPreview_save.py: out-hist-mrg(md) ---> out-hist-mrg-html(html)
#

hist-all:
	python ../history.py -q questions -c chats -o out-hist-mrg -t out-hist-mrg-txt --merge
	python ../subl_markdownPreview_save.py -i out-hist-mrg -o out-hist-mrg-html

hist-all-pdf:
	python ../topdf.py -i out-hist-mrg-html -o out-hist-mrg-pdf

clean-hist:
	rm -rf out-hist-cht 
	rm -rf out-hist-cht-html 
	rm -rf out-hist-cht-pdf 
	rm -rf out-hist-qst 
	rm -rf out-hist-qst-html 
	rm -rf out-hist-qst-pdf 
	rm -rf out-hist-mrg 
	rm -rf out-hist-mrg-txt 
	rm -rf out-hist-mrg-html 
	rm -rf out-hist-mrg-pdf 	

build-hist: hist-qst hist-cht hist-all

build-all: chat2md build build-hist

clean-ans:
	rm -rf out-ans 
	rm -rf out-ans-html 
	rm -rf out-ans-pdf 

clean-hist:
	rm -rf out-hist-cht 
	rm -rf out-hist-cht-html 
	rm -rf out-hist-cht-pdf 
	rm -rf out-hist-qst 
	rm -rf out-hist-qst-html 
	rm -rf out-hist-qst-pdf 
	rm -rf out-hist-mrg 
	rm -rf out-hist-mrg-txt 
	rm -rf out-hist-mrg-html 
	rm -rf out-hist-mrg-pdf 

clean-all: clean-ans clean-hist

#
# Daily report
#	

daily: chat2md update hist-all

daily-pdf: chat2md update hist-all hist-all-pdf


	
