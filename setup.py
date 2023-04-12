# {
#     "name": "useful",
#     "version": "1",
#     "description": "Very useful code",
#     "url": "http://github.com/dummy_user/useful",
#     "author": "Flying Circus",
#     "author_email": "flyingcircus@example.com",
#     "license": "MIT",
#     "packages": ["useful"],
# }

from setuptools import find_packages, setup, find_namespace_packages

setup (name='sort_pack',
       version='0.0.1',
       description='Sort file - garbage',
       url='',
       author='Igor Gievskiy',
       author_email='sillahed@gmail.com',
       license='GiGaS',
       packages=find_packages(),
       entry_points={'console_scripts':['hello = sort_pack:sort']},
       include_package_data=True
       )

    
    


