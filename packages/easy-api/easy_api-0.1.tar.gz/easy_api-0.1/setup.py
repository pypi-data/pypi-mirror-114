from distutils.core import setup
setup(
  name = 'easy_api',         # How you named your package folder (MyLib)
  packages = ['easy_api'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a easy-to-use library of APIs',   # Give a short description about your library
  author = 'Samuel Cheng',                   # Type in your name
  author_email = 'samuelcheng000@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/mime-r/easy_api',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mime-r/easy_api/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['api', 'apis', 'easy'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'json',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
