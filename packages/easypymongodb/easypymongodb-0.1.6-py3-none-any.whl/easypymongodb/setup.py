import setuptools

with open("easypymongodb/README.md", "r") as fhandle:
    long_description = fhandle.read() # Your README.md file will be used as the long description!

setuptools.setup(
  name="easypymongodb", # Put your username here!
  version="0.1.6", # The version of your package!
  author="Zeliktric", # Your name here!
  author_email="zeliktric@gmail.com", # Your e-mail here!
  description="A package that simplifies the use of the pymongo library.", # A short description here!
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Zeliktric/easypymongodb", # Link your package website here! (most commonly a GitHub repo)
  packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ], # Enter meta data into the classifiers list!
  python_requires=">=3.6", # The version requirement for Python to run your package!
  keywords = ["DB", "database", "mongo", "pymongo", "easypymongodb", "python", "db"],
  install_requires=[            
    "pymongo",
    "dnspython"
  ],
)
