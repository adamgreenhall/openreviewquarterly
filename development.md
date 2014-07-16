This is a guide to getting the orq up and running for development on Mac OSX.

# Software tools you will need

* [Xcode command line tools](http://www.kennethreitz.org/essays/xcode-gcc-and-homebrew)
* [git](http://git-scm.com/)
* [rbenv](https://github.com/sstephenson/rbenv)
* [heroku toolbelt](https://toolbelt.heroku.com/)


## The easy way to get these things
### OSX command line tools
Command line tools are OSX version specific:
* for Mountain Lion (or more recent), just open the terminal and type ``gcc``. If command line tools aren't installed, you will get a [prompt](http://railsapps.github.io/images/installing-mavericks-popup.png) asking if you want to install them. You do.
* for Lion (or less recent), you'll have to go to [http://developer.apple.com/downloads](http://developer.apple.com/downloads), login, search for **Command Line Tools for Xcode**, download it, and run the installer. 

### Everything else
You can use the terminal to install everything else:

	# homebrew - helps to install other things
	ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)" 
	# git, rbenv
	brew install git rbenv ruby-build
	# heroku toolbelt
	wget -qO- https://toolbelt.heroku.com/install.sh | sh


# Getting the ORQ running for the first time
	# first install ruby
	rbenv install $(cat .ruby-version)
	# then bundler
	gem install bundler
	# install the orq gems
	bundle
	# you will need a postgres user named orq
	createuser orq -d -s -h localhost
	# create database
	rake db:create
	rake db:migrate
	# get a fresh copy of the database
	heroku pgbackups:capture # if this fails, it's ok, just keep going
	curl -o latest.dump `heroku pgbackups:url`
	pg_restore --verbose --clean --no-acl --no-owner -h localhost -U orq -d orq latest.dump