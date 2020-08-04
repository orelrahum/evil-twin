#!/usr/bin/make -f
git:
    git add -A
    git commit -m "commit"
    git push -u origin master 

clean:
	rm -f *.pdf