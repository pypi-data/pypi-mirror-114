from distutils.core import setup
setup(
  name = 'easy_widgets',
  packages = ['easy_widgets'], # this must be the same as the name above
  version = '0.2',
  description = 'Make widget management in CLI easy',
  author = 'Stefan Nozinic',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/easy_widgets', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/easy_widgets/tarball/0.2', 
  keywords = ['curses'], # arbitrary keywords
  package_dir = {'easy_widgets': 'src'},
  classifiers = [],
)
