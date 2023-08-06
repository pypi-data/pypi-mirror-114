from distutils.core import setup
setup(
  name = 'youtube-uploader-selenium-aug',         # How you named your package folder (MyLib)
  packages = ['youtube_uploader_selenium'],   # Chose the same as "name"
  version = '1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'youtube-uploader-selenium dependency works August 2021',   # Give a short description about your library
  author = 'M4rkoHR',                   # Type in your name
  author_email = 'markovukadin3@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/M4rkoHR/youtube_uploader_selenium/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/M4rkoHR/youtube_uploader_selenium/',    # I explain this later on
  keywords = ['youtube', 'upload', 'selenium'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium_firefox',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',
  ],
)