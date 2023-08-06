from distutils.core import setup
setup(
  name = 'newrl',
  packages = ['newrl'],
  version = '0.1',
  license='MIT',
  description = 'Python SDK for Newrl blockchain',
  author = 'Kousthub Raja',
  author_email = 'kousthub@asqi.in',
  url = 'https://github.com/asqi/newrl',
  download_url = 'https://github.com/asqisys/newrl-py/archive/refs/tags/v_02.tar.gz',
  keywords = ['newrl', 'blockchain', 'client'],
  install_requires=[],
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