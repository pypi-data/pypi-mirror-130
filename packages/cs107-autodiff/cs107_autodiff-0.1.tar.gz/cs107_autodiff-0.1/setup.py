from setuptools import setup, find_packages
setup(
  name = 'cs107_autodiff',         # How you named your package folder (MyLib)
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automated Differentiation based on forward and reverse mode',   # Give a short description about your library
  author = 'ShangShang Wang, Max Urbany, Meghna Banerjee, Mingcheng(Jason) Liu',                   # Type in your name
  author_email = '',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  packages=find_packages('src'),
  package_dir={'': 'src'},
  download_url = '',    # I explain this later on
  keywords = ['FORWARD MODE', 'BACKWARD MODE', 'DERIVATIVES'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pytest'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)