# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Usage:             ``from khoros.utils import core_utils``
:Example:           ``encoded_string = core_utils.encode_url(decoded_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     20 Feb 2020
"""

import urllib.parse


def url_encode(raw_string):
    """This function encodes a string for use in URLs.

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    """
    return urllib.parse.unquote_plus(encoded_string)


def encode_query_string(url_dict):
    """This function compiles a URL query string from a dictionary of parameters.

    :param url_dict: Dictionary of URL query string keys and values
    :type url_dict: dict
    :returns: The URL query string in string format
    """
    return urllib.parse.urlencode(url_dict)