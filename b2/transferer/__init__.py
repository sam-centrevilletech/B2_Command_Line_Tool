######################################################################
#
# File: b2/transferer/__init__.py
#
# Copyright 2019 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

from b2sdk.transferer import *  # noqa

import b2._sdk_deprecation
b2._sdk_deprecation.deprecate_module('b2.transferer')
