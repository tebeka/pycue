from setuptools import setup


def version():
    with open('cue.py') as fp:
        for line in fp:
            if line.startswith('__version__'):
                _, version = line.split('=')
                return version.replace("'", '').strip()


def load_deps(file_name):
    """Load dependencies from requirements file"""
    deps = []
    with open(file_name) as fp:
        for line in fp:
            line = line.strip()
            if not line or line[0] == '#' or line.startswith('-r'):
                continue
            deps.append(line)
    return deps


install_requires = load_deps('requirements.txt')
tests_require = load_deps('dev-requirements.txt')

with open('README.md') as fp:
    long_desc = fp.read()

setup(
    name='pycue',
    version=version(),
    description='Python wrapper for https://cuelang.org',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Miki Tebeka',
    author_email='miki@353solutions.com',
    license='MIT',
    url='https://github.com/tebeka/cue',
    py_modules=['cue'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    tests_require=tests_require,
)
