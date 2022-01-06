## Notes: Lecture 1 Git

## Git
A command-line tool for version control, to track changes to a file over time by
taking snapshots of the code and reference the changes.  
Also lets us sync code between many people working on the same project.  

Code is stored in a repository, which holds all the files of a project.
Developers make changes to files as they work, and whent they're done, they
"push" their changes back to the repo, so that the repo is synced with the most
up-to-date version of code.  
Developers then "pull" the most up-to-date version of the code to start the next
work.
Git also allows us to create branches, so that we can make changes to code and
then test those changes to see if the work, without losing a working version of
the code before we know the changes are good.  
If the changes I've made are bad, we can revert back to a previous version of
code.


## Github  
Code needs to be hosted, and the most popular hosting service is Github.  
www.github.com/new to create a new repo, names in repos must be unique.  
```git clone <url>```: Copy (download) a remote repo from the url to a local
repo in the folder you're in.  
Forking: Making a new repo in your github account that is a copy of someone
else's repo  
Github pages: A free, static website hosting service from Github   


## Commits  
Saving files is a 2-step process: files must be tracked/staged via ```add``` and
then ```commit```ed.  
```git add <file> or <.>```: Tell Git to start tracking the ```<file>``` or the
whole directory (```<.>```). This moves the files to the staging area.  
```git commit -m "message"```: Tell git to save a snapshot of the current state
of the repo, along with a short message describing the changes you've made.  
```git status```: Find out your status/commit position relative to
origin/master, the main branch.  
```git push```: Push the changes you made in your commit to your localbranch/master
branch to the origin/master branch  
```git commit -am "message"```: Shortcut to run ```Git commit all files "message"```  
```git pull```: Get most recent version of code from origin/master branch  
First commit message is often "First commit"  

## Merge Conflicts  
If the origin/master branch has new changes before you commit your changes, you
may have a merge conflict, because your local version will not reflect the most
recent changes. This conflict needs to be resolved before you can merge your
changes to the origin/master branch.  
First, remove merge conflict notes from git.  
Then, edit code to resolve the conflict.  
Other options include "accept current" or "accept incoming" changes

```git log```: Track all changes made to your code, describing all the commits
in a repo.  
  Each commit description will have a hash signature of the commit, the author
of the commit, the commit's date, and the commit's message

```git reset```: take the current state of the repo and revert it to an earlier
state  
```git reset --hard <commit hash>```: reset to an earlier commit, by hash  
```git reset --hard origin/master```: reset to the origin/master repo 


## Branching  
How to handle non-linear work, aka fixing multiple unrelated bugs or features:
branching
Create a new branch for a specific purpose  
master branch: main, released branch  
feature branch: a side, feature-related branch  
HEAD: the most recent commit on a branch  
Merge: syncing the head of a feature branch with the head of the master branch  

```git branch```: tells me what branch I'm working on  
```git checkout - b <name>```: create and switch to a new branch, called ```<name>```  
```git checkout <name>```: switch to an already-existing branch ```<name>```