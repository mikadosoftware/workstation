Making keys for github
----------------------

In order to push code up to GitHub, I need a private / public key pair for ssh.
::

  ssh-keygen -l -f sshkey -E md5
  ssh-keygen -t rsa -b 4096 -C paul@mikadosoftware.com

I name the keypair `common-github`.  The keys are in my ~/.ssh folder.
I visit www.github.com and in my settings add the *public* key to have permissions on my account

Now I setup .ssh/config file like this::

  Host github.com
      User git
      IdentityFile ~/.ssh/common-github

If I then run ::

  ssh -T git@github.com -i .ssh/common-github

I get access approval message and all is good.

