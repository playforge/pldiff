#!/usr/bin/env python

import distutils.core

distutils.core.setup(
    name='pldiff',
    version='1.0.1',
    description='Structured Data Diffing',
    author='Stephen Altamirano',
    author_email='stephen@theplayforge.com',
    packages=['libpldiff']
)