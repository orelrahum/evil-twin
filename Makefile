#!make -f

all: 
	git pull
	git add -A
	echo Pls enter your commit
	read varname
	git commit -m $varname
	git push -u origin master

clean:
	rm -f *.out a.out


