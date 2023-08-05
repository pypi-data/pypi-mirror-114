from distutils.core import setup
setup(
  name = 'leapfrogmshreader',        
  packages = ['leapfrogmshreader'],  
  #package_dir={"":"src"},
  version = '0.22',      
  license='LGPL 3.0',       
  description = 'A simple reader of leapfrog mesh files, without onerous installation requirements.',  
  author = 'Thomas Martin',                  
  author_email = 'tpm319@gmail.com',      
  url = 'https://github.com/ThomasMGeo/leapfrog_msh_reader',     
  keywords = ['leapfrog', 'mesh', '.msh'],   
  install_requires=[   ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',  
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)