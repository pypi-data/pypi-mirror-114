from setuptools import setup

with open("README.md", encoding="utf-8") as file:
  long_desc = file.read()

setup(
  name = 'scarletdb',         # How you named your package folder (MyLib)
  packages = ['scarletdb'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make,
  description = "Light document database.",
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_desc,
  long_description_content_type="text/markdown",
  author = 'Finnbar McC',                   # Type in your name
  author_email = 'xfinnbar@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/xd-pro/scarletdb',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Xd-pro/ScarletDB/archive/refs/tags/0.1-beta.tar.gz',    # I explain this later on
  keywords = ['db', 'database', 'scarlet'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'replit',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)