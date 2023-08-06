from setuptools import setup

setup(
    name='lp2ply',
    version='0.1',
    description='Transform lamination parameters into stacking sequences.',
    author='Moritz Sprengholz',
    author_email='m.sprengholz@tu-bs.de',
    url="https://git.rz.tu-bs.de/m.sprengholz/publication-lamination-parameters",
    packages=['lp2ply'],
    install_requires=[
        'numpy',
        'DFO-LS',
        'numba',
        'pyDOE',
    ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

