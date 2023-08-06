from distutils.core import setup
setup(
  name = 'autodiffad',         
  packages = ['autodiffad'],   
  version = '1.0.3',      
  license='MIT',        
  description = 'Automatic Differentiation',   
  author = 'cs107-zero-day-exploit',                   
  author_email = 'yichunyao@hsph.harvard.edu',      
  url = 'https://github.com/cs107-zero-day-exploit/cs107-FinalProject',   
  download_url = 'https://github.com/cs107-zero-day-exploit/cs107-FinalProject/archive/refs/tags/v1.0.3.tar.gz',
  keywords = ['automatic', 'differentiation', 'forward mode', 'reverse mode'],   
  install_requires=[            
          'numpy',
          'pytest',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
