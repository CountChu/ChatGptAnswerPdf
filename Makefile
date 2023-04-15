answer-1:
	python answer.py -q "questions-230402/230327.OP-TEE.SP.txt" -c "chats-manual" -a "output"

answer-2:
	python answer.py -q "questions-230402/230327.OP-TEE.txt" -c "chats-manual" -a "output"

answer-3:
	python answer.py -q "questions-230402/230329.TrustZone.txt" -c "chats-manual" -a "output"

answer-4:
	python answer.py -q "questions-230402/230330.OP-TEE.j721e.txt" -c "chats-manual" -a "output"

answer-5:
	python answer.py -q "questions-230402/230330.OP-TEE.Intel.txt" -c "chats-manual" -a "output"

answer-6:
	python answer.py -q "questions-230402/230330.Questions.txt" -c "chats-manual" -a "output"

answer-7:
	python answer.py -q "questions-230402/230402.DRM.txt" -c "chats-manual" -a "output"

answer-all: answer-1 answer-2 answer-3 answer-4 answer-5 answer-6 answer-7

tohtml:
	python tohtml.py -i output -o output-html

topdf:
	python topdf.py -i output-html -o output-pdf

update:
	python chatpdf.py update

build:
	python chatpdf.py build

chat2md:
	rm -rf chats
	python chat2md.py -i download-230414 -o chats

clean:
	rm -rf output 
	rm -rf output-html 
	rm -rf output-pdf 




