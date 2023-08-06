from distutils.core import setup

setup(
  name = 'cherrypie_flask',
  packages = ['cherrypie_flask'],
  version = '0.2',
  license='MIT',
  description = 'CherryPie Flask SDK',
  author = 'MacroComputerClub',
  author_email = 'support@cherrypie.app',
  url = 'https://github.com/Macro-Computer-Club/cherrypie-flask',
  download_url = 'https://github.com/Macro-Computer-Club/cherrypie-flask/archive/refs/tags/v0.1.tar.gz',
  keywords = ['CHERRYPIE', 'FLASK', 'SDK'],
  install_requires=[
    'requests',
    'urllib3',
    'flask',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
