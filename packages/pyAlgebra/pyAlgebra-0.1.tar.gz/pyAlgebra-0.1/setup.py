from setuptools import setup
    
setup(name="pyAlgebra", 
      version="0.1", 
      url="https://github.com/prakHr/pyAlgebra-v",
      download_url="https://github.com/prakHr/pyAlgebra-v/archive/refs/tags/v01.tar.gz",
      install_requires=[            # I get to this in a second
          'sympy',
          'matplotlib',
      ],
      maintainer='Prakhar Gandhi',
      maintainer_email='gprakhar0@gmail.com',
      py_modules=['pyAlgebra'],
      description="performs integral and differentiable operations on string expressions using sympy") 
