import versioneer
from distutils.core import setup

setup(name='cmgibs',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Dalton R. Kell/Brian McKenna',
      author_email=['dalton.kell@rpsgroup.com', 'brian.mckenna@rpsgroup.com'],
      description='NASA colormaps powered by Python',
      long_description=open('README.md').read(),
      install_requires=[
          'lxml>=4.2.3',
          'matplotlib>=2.2.2',
          'numpy>=1.14.5'
      ]
)
