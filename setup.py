from setuptools import find_packages, setup


setup(
    name='whoseline-vis',
    version='0.1.0',
    url='https://github.com/bmorris3/whoseline-vis',
    license='BSD',
    author='Whose Line Hack Group',
    author_email='',
    description='',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "astropy",
        "bokeh",
        "Flask",
        "Jinja2",
        "numpy",
        "pandas",
        "six"
    ],
    entry_points = {
        'console_scripts': ['wlv=whoseline_vis.__init__:start'],
    }
)
