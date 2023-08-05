from setuptools import setup, Extension

latest_version = "1.0.1"

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'champion-name-converter',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages = ['champion-converter'],   
  version = latest_version,
  license='MIT',
  description = 'Convert League of Legends Champions Name to ID',   
  author = 'flowd1337',                   
  author_email = 'john_doe@gmail.com',      
  url = 'https://github.com/flowd1337/champion-name-converter/',   
  download_url = 'https://github.com/flowd1337/champion-name-converter/archive/refs/tags/{}.tar.gz'.format(latest_version),
  keywords = ['League', 'League of Legends', 'Champion Name Converter'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
  ],
)
