from setuptools import setup, find_packages

# I want my readme to be part of the setup, so let's read it.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

      # this will be my Library name.
      name='wordhunt-anagram-search-python',

      # Want to make sure people know who made it.
      author='Immanuel Adotey Allotey',

      # also an email they can use to reach out.
      author_email='imma.adt@gmail.com',

      # I'm in alpha development still, so a compliant version number is a1.
      # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
      version='0.1.0.dev3',

      # here is a simple description of the library, this will appear when someone searches for the library on https://pypi.org/search
      description='A python client library for word search in games like iMessage wordhunt and anagram.',

      # I have a long description but that will just be my README file, note the variable up above where I read the file.
      long_description=long_description,

      # want to make sure that I specify the long description as MARKDOWN.
      long_description_content_type="text/markdown",

      # here is the URL you can find the code, this is just the GitHub URL.
      url='https://github.com/bstudiosoriginal/WordHuntAnagram',

      # there are some dependencies to use the library, so let's list them out.
      install_reqs = [],

      # some keywords for my library.
      keywords = 'word games, word search, anagram, wordhunt, iMessage games',

      # here are the packages I want "build."
      packages=find_packages(include=['wordhuntanagram',]),

      # additional package data
      package_data={
          "wordhuntanagram": ["data/*", "logs", "words.json"]
      },

      # I also have some package data, like photos and JSON files, so I want to include those too.
      include_package_data=True,

      # additional classifiers that give some characteristics about the package.
      classifiers=[

            # I want people to know it's still early stages.
           'Development Status :: 3 - Alpha',

            # My Intended audience is mostly those who understand finance.
           'Intended Audience :: End Users/Desktop',

           # My License is MIT.
           'License :: OSI Approved :: MIT License',

           # I wrote the client in English
           'Natural Language :: English',

           # The client should work on all OS.
           'Operating System :: OS Independent',

           # The client is intendend for PYTHON 3
           'Programming Language :: Python :: 3 :: Only',
           'Programming Language :: Python :: 3.5',
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
           'Programming Language :: Python :: 3.9'
      ],

      # you will need python 3.5 to use this libary.
      python_requires='>=3.5'

     )