#! /usr/bin/env python
# Copyright © 2019 Uwe Schitt <uwe.schmitt@id.ethz.ch>

import pkg_resources

__version__ = tuple(map(int, pkg_resources.require(__package__)[0].version.split(".")))
