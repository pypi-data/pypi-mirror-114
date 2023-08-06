from setuptools import setup

setup(
    name='marshmallow-helpers',
    version='0.4.4',
    packages=['marshmallow_helpers',
              'marshmallow_helpers.marshmallow_annotations',
              'marshmallow_helpers.marshmallow_annotations.ext'],
    author_email="zidder@hilearn.io",
    description="Ease marshmallow schema creation",
    classifiers=['Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha'],
    install_requires=["attrs==20.3.0",
                      "marshmallow>=3.5.1",
                      "webargs>=5.5.3"],
    extras_require={
        "model": ["sqlalchemy>=1.3.20"]
    },
    dependency_links=["https://github.com/hilearn/marshmallow-annotations"]
)
