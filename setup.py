from setuptools import setup

setup(
    name             = 'ep-sphere_mesh',
    version          = '0.0.1',
    description      = 'A ChRIS ds plugin wrapper for sphere_mesh',
    author           = 'Jennings Zhang',
    author_email     = 'Jennings.Zhang@childrens.harvard.edu',
    url              = 'https://github.com/FNNDSC/ep-sphere_mesh',
    py_modules       = ['sphere_mesh_wrapper'],
    install_requires = ['chris_plugin', 'pycivet'],
    license          = 'MIT',
    python_requires  = '>=3.10.2',
    entry_points     = {
        'console_scripts': [
            'sphere_mesh_wrapper = sphere_mesh_wrapper.app:main'
            ]
        },
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
