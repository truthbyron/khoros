# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Usage:             ``from khoros.errors import handlers``
:Example:           ``error_msg = handlers.get_error_from_html(html_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Feb 2020
"""

import re


def get_error_from_html(html_error):
    """This function parses an error message from Khoros displayed in HTML format.

    :param html_error: The raw HTML returned via the :py:mod:`requests` module
    :type html_error: str
    :returns: The concise error message parsed from the HTML
    """
    error_title = re.sub('</h1>.*$', '', re.sub('^.*<body><h1>', '', html_error))
    error_description = re.sub('</u>.*$', '', re.sub('^.*description</b>\s*<u>', '', html_error))
    return f"{error_title}{error_description}"