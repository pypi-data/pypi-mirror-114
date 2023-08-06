from distutils.core import setup
setup(
  name = 'pyphotonics',         # How you named your package folder (MyLib)
  packages = ['pyphotonics'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The PyPhotonics python code is a post-processing code written entirely in python which takes as input the output files of the VASP and phonopy codes for a defect system, and calculates the Huang-Rhys factor and the PL lineshapes for that system.',   # Give a short description about your library
  author = 'Sherif Abdulkader Tawfik',                   # Type in your name
  author_email = 'sherif.tawfic@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sheriftawfikabbas/pyphotonics',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['DFT', 'Material science', 'Photoluminescence', 'VASP'],   # Keywords that define your package best
  install_requires=['scipy','sys','numpy','pandas','matplotlib'],

)