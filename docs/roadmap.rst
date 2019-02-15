Roadmap
=======

I recently posted this project to Hacker News (Front Page!!!) and was pleasantly surprised by the positive response.  And so I feel a responsibility to actually improve the project and start ironing out bugs.

This is then my roadmap for the next couple of weeks (well probably months)

Milestones 
==========

* Review of literature.
  A lot of similar projects have been mentioned - it is well worth covering the good bad and ugly and using that to inform the roadmap

* Single point of entry
  A simple python CLI that will do the work of detecting OS somslighlty modified docker commands can run etc etc

* Clean up docs

* split out the (very) specific hardcoded usernames etc

* look at recipes / methods to build the final Dockerfile and make it more robust without losing the basic "it's just string formatting" part

* Marketing 
  well this was supposed to be just a personal project, and I don't see it as being the next big thing.  But enough people have noticed that it should be polished and given a run round the block.  Once it's stops being fun I will stop :-)

It also seems a good idea to use it for the "plumbing" portion of my new book - that is the dev and CI cycle
I should have this as an exemplar dev / CI cycle - so 

* pre-commit hooks ensuring, lint, test, formatting, doc
* Jenkins build on AWS leading to CI, docker deployment (err how??)
* docs build

SImilar cases can be made for rewriting the CMS, and adding FIDO to the CMS


