from distutils.core import setup
setup(
  name = 'oscar_tools',         # How you named your package folder (MyLib)
  version = '0.0.18',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Recording tools for ',   # Give a short description about your library
  author = 'Alberto Occelli',                   # Type in your name
  author_email = 'albertoccelli@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/albertoccelli/Oscar_Tools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/albertoccelli/Oscar_Tools/archive/refs/tags/0.0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['HATS', 'RECORD', 'WAV'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        "cycler==0.10.0",
        "kiwisolver==1.3.1",
        "matplotlib==3.4.2",
        "numpy==1.21.0",
        "Pillow==8.3.0",
        "pydub==0.25.1",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "scipy==1.7.0",
        "six==1.16.0",
        "sympy==1.8",
        "requests==2.25.1",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  package_dir={"":"source"}
)
