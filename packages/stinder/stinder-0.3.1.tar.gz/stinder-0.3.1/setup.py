import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setuptools.setup(
    name='stinder',
    version='0.3.1',
    description='The Stinder project aims to help students find compatible study partners through their major and coursework for optimal study sessions.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/gibbons-eddie/Stinder',
    install_requires=['numpy>=1.21.0', 'PySide6>=6.1.1'],
    author='Eddie Gibbons, Allison Denham, Carlos Echenique, Wyatt Townsend, Yuchen Xiong',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],
    packages=setuptools.find_namespace_packages(include=['stinder', 'stinder.*']),
    package_data={'':['*.db', '*.otf', '*.qrc', '*.png', '*.jpg']},
    python_requires='>=3.8.2',
    entry_points={
        'console_scripts': [
            'Stinder = stinder.__main__:main',
        ]
    }
)