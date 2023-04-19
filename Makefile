answer-1:
	python answer.py -q "questions-230402/230327.OP-TEE.SP.txt" -c "chats-manual" -a "out-ans"

answer-2:
	python answer.py -q "questions-230402/230327.OP-TEE.txt" -c "chats-manual" -a "out-ans"

answer-3:
	python answer.py -q "questions-230402/230329.TrustZone.txt" -c "chats-manual" -a "out-ans"

answer-4:
	python answer.py -q "questions-230402/230330.OP-TEE.j721e.txt" -c "chats-manual" -a "out-ans"

answer-5:
	python answer.py -q "questions-230402/230330.OP-TEE.Intel.txt" -c "chats-manual" -a "out-ans"

answer-6:
	python answer.py -q "questions-230402/230330.Questions.txt" -c "chats-manual" -a "out-ans"

answer-7:
	python answer.py -q "questions-230402/230402.DRM.txt" -c "chats-manual" -a "out-ans"

answer-all: answer-1 answer-2 answer-3 answer-4 answer-5 answer-6 answer-7

tohtml:
	python tohtml.py -i out-ans -o out-ans-html

topdf:
	python topdf.py -i out-ans-html -o out-ans-pdf

update:
	python chatpdf.py update

build:
	python chatpdf.py build

chat2md:
	rm -rf chats
	python chat2md.py -i download-230419 -o chats

hist-qst:
	python history.py -q questions -c chats -o out-hist-qst
	python tohtml.py -i out-hist-qst -o out-hist-qst-html
	#python topdf.py -i out-hist-qst-html -o out-hist-qst-pdf

hist-cht:
	python history.py -c chats -o out-hist-cht
	python tohtml.py -i out-hist-cht -o out-hist-cht-html
	#python topdf.py -i out-hist-cht-html -o out-hist-cht-pdf

hist-all:
	python history.py -q questions -c chats -o out-hist-mgr --merge
	python tohtml.py -i out-hist-mgr -o out-hist-mgr-html
	#python topdf.py -i out-hist-mgr-html -o out-hist-mgr-pdf

clean:
	rm -rf out-ans 
	rm -rf out-ans-html 
	rm -rf out-ans-pdf 
	rm -rf out-hist-cht 
	rm -rf out-hist-cht-html 
	rm -rf out-hist-cht-pdf 
	rm -rf out-hist-qst 
	rm -rf out-hist-qst-html 
	rm -rf out-hist-qst-pdf 



