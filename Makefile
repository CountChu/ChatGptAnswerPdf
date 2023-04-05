answer-1:
	python answer.py -q "questions/230327 OP-TEE - SP.txt" -c "chats" -a "output"

answer-2:
	python answer.py -q "questions/230327 OP-TEE.txt" -c "chats" -a "output"

answer-4:
	python answer.py -q "questions/230329 TrustZone.txt" -c "chats" -a "output"

answer-5:
	python answer.py -q "questions/230330 OP-TEE - j721e.txt" -c "chats" -a "output"

answer-6:
	python answer.py -q "questions/230330 OP-TEE - Intel.txt" -c "chats" -a "output"

answer-7:
	python answer.py -q "questions/230330 Questions.txt" -c "chats" -a "output"

answer-8:
	python answer.py -q "questions/230402 DRM.txt" -c "chats" -a "output"

answer-all: md1 md2 md3 md4 md5 md6 md7 md8

tohtml:
	python tohtml.py -i output -o output-html

topdf:
	python topdf.py -i output-html -o output-pdf

tohtml-3:
	python tohtml.py -f 230328.TEE.md -i output -o output-html
	
topdf-3:
	python topdf.py -f 230328.TEE.html -i output-html -o output-pdf		

output-pdf/230328.TEE.pdf: questions/230328.TEE.txt chats/TEE.0328.md
	python chatpdf.py build -f 230328.TEE.txt 

chatpdf-3: output-pdf/230328.TEE.pdf

refresh:
	python chatpdf.py refresh


