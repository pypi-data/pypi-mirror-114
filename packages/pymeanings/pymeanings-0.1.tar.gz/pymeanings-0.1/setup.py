from setuptools import setup

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(name='pymeanings',
      version='0.1',
      description='Getting meanings in a GUI dailog box',
      long_description=readme(),
      url='https://github.com/adhrit2019/pymeanings',
      author='Adhrit Pramanik',
      author_email='adhrit2019@gmail.com',
      license='MIT',
      packages=['pymeanings'],
      install_requires=['PyDictionary'],
      zip_safe=False,
      entry_points={
                    'console_scripts':['pymeaning=pymeanings.command_line:main']
      })
