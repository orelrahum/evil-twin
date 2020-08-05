#!make -f

all: 
	git add -A
	git commit -m "commit"
	git push -u origin master


clean:
	rm -f *.out a.out


