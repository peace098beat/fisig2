# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


version = {
    "0.0.1":"First Commit",
    "0.1.0":"Covered Python3",
    "0.2.0":"Directory Sirialize",
}

# def main():
#     description = 'fisig2'

#     setup(
#         name='fisig2',
#         version='0.2.0',
#         author='tomoyuki nohara',
#         author_email='tomoyuki_nohara@example.jp',
#         url='www.tomoyuki_nohara.jp',
#         description=description,
#         long_description=description,
#         zip_safe=False,
#         include_package_data=True,
#         packages=find_packages(),
#         install_requires=["pyaudio","scipy","numpy"],
#         tests_require=[],
#         setup_requires=[],
#     )

import sys
sys.path.append('./test')
def main():
    description = 'fisig2 is signal analysis package'

    setup(
        name='fisig2',
        version='0.2.0',
        author='tomoyuki nohara',
        author_email='tomoyuki_nohara@example.jp',
        url='www.tomoyuki_nohara.jp',
        description=description,
        long_description=description,
        packages=find_packages("fisig2"),
        package_dir={'': 'fisig2'},
        install_requires=["pyaudio","scipy","numpy"],
    )
if __name__ == '__main__':
    main()