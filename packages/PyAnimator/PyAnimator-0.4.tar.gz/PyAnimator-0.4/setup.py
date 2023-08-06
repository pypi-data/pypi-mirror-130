from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'PyAnimator',         # How you named your package folder (MyLib)
  packages = ['PyAnimator'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Create awesome animation's with only one line of code !",   # Give a short description about your library
  author = 'AzgarD',                   # Type in your name
  author_email = 'anon@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/AzgarDev/animator',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AzgarDev/animator/archive/v_0.3.tar.gz',    # I explain this later on
  keywords = ['Animation', 'RGB animation python', 'Python rgb animation'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'colorama'
      ],
  long_description=long_description,
  long_description_content_type='text/markdown',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
