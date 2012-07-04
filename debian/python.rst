Actually came back with some feedback to my own question. 

The following repositories do the job: 

# /etc/apt/sources.list 
deb http://ftp.uk.debian.org/debian/ unstable main contrib non-free 
deb http://ftp.uk.debian.org/debian/ experimental main contrib non-free 
deb http://security.debian.org/ testing/updates main contrib 

$ apt-get update 
$ apt-get install python2.7 
$ python --version 
Python 2.6.6 
$ python2.7 --version 
Python 2.7.1+ 

If you need 2.7 as default runtime: 

$ update-alternatives --install /usr/bin/python python /usr/bin/python2.7 10 

This is the first time I need two Python instances, so might helpful for 
someone in the same position. Any further help feel free to reply. 

Cheers. 
