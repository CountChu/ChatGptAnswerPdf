answer:
	python ../answer.py -q "questions-230402/230327.OP-TEE.SP.yaml" -c "chats-manual" -a "out-ans"

tohtml:
	python ../tohtml.py -i out-ans -o out-ans-html

topdf:
	python ../topdf.py -i out-ans-html -o out-ans-pdf

.PHONY: update
update:
	python ../chatpdf.py update

chat2md:
	python ../chat2md.py -i download-230421 -o chats

build:
	python ../chatpdf.py build

hist-qst:
	python ../history.py -q questions -c chats -o out-hist-qst
	python ../tohtml.py -i out-hist-qst -o out-hist-qst-html
	python ../topdf.py -i out-hist-qst-html -o out-hist-qst-pdf

hist-cht:
	python ../history.py -c chats -o out-hist-cht
	python ../tohtml.py -i out-hist-cht -o out-hist-cht-html
	python ../topdf.py -i out-hist-cht-html -o out-hist-cht-pdf

hist-all:
	python ../history.py -q questions -c chats -o out-hist-mrg -t out-hist-mrg-txt --merge
	python ../tohtml.py -i out-hist-mrg -o out-hist-mrg-html
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

build-all: build build-hist

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

txt2yaml:
	python ../txt2yaml.py -i questions-txt -o questions 


