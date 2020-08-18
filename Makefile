#!make -f

all: 
	git pull
	git add -A
	git commit -m "commitfrom kali"
	git push -u origin master

clean:
	rm -f *.out a.out


