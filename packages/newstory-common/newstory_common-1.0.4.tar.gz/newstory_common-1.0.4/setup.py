from setuptools import setup, find_packages
setup(name='newstory_common',
      version='1.0.4',
      description='Common modules for Newstory',
      url='https://pypi.org/project/newstory_common',
      author='Eylon Ronen',
      author_email='eylon.ronen@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            "Pillow"
      ],
      zip_safe=False)
