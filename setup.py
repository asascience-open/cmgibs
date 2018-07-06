import versioneer
setup(name='cmnasa',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Dalton R. Kell/Brian McKenna',
      description='NASA colormaps powered by Python',
      long_description=open(README.md).read(),
      install_requries=[
          'lxml==4.2.3',
          'matplotlib==2.2.2',
          'numpy==1.14.5'
      ]
)
