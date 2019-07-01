Roadmap
=======

I recently posted this project to Hacker News (Front Page!!!) and was
pleasantly surprised by the positive response.  And so I feel a
responsibility to actually improve the project and start ironing out
bugs.

This is then my roadmap for the next couple of weeks (well probably
months)

Milestones 
==========

* Review of literature.
  A lot of similar projects have been mentioned - it is well worth covering the good bad and ugly and using that to inform the roadmap

* Single point of entry
  A simple python CLI that will do the work of detecting OS somslighlty modified docker commands can run etc etc
  (This has been the bulk of work here - really that took waaaay longer than I expected, epecially
  with just doing this on commutes etc.)

* Clean up docs
  Still to do

* split out the (very) specific hardcoded usernames etc
  Mostly done I think


* look at recipes / methods to build the final Dockerfile and make it
  more robust without losing the basic "it's just string formatting"
  part
  Yeah thats ok. ish

* Marketing

  well this was supposed to be just a personal project, and I don't
  see it as being the next big thing.  But enough people have noticed
  that it should be polished and given a run round the block.  Once
  it's stops being fun I will stop :-)


* pre-commit hooks ensuring, lint, test, formatting, doc
  I use black ... does that count? No? Ok..
  


2019
----

The plan here is to incorporate a very good suggestion by @bjornicus (#6)
I relly do owe them an apology - early users should be gold.

Then keep on dogfooding - its *usable* by me - some glitches
(especially around the use of `sleep` and also failing to see the
error response sent by sshd if there is an error (usually its the MiTM
attack warning).

