from setuptools import setup
import re

requirements = ["requests"]
version = '0.2.3'
readme = open('README.md').read()
extras_require = {}

setup (
        name='selfcord',
        author='Benny',
        url='https://github.com/ilyBenny/selfcord',
        project_urls={},
        version=version,
        packages=['selfcord'],
        license='MIT',
        description='The best Discord selfbot API wrapper.',
        long_description=readme,
        long_description_content_type="text/markdown",
        include_package_data=True,
        install_requires=requirements,
        extras_require=extras_require,
        python_requires='>=3.8.0',
        classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
        ]
      )
