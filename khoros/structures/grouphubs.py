# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.grouphubs
:Synopsis:          This module contains functions specific to group hubs within the Khoros Community platform
:Usage:             ``from khoros.structures import grouphubs``
:Example:           ``group_hub_url = grouphubs.create(khoros_object, gh_id, gh_title, disc_styles, return_url=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     27 May 2020
"""

from .. import api, errors


VALID_DISCUSSION_STYLES = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']


def create(khoros_object, group_id, group_title, description=None, membership_type=None, open_group=None,
           closed_group=None, hidden_group=None, discussion_styles=None, enable_blog=None, enable_contest=None,
           enable_forum=None, enable_idea=None, enable_qanda=None, enable_tkb=None, all_styles_default=True,
           parent_category_id=None, avatar_image_path=None, full_response=None, return_id=None, return_url=None,
           return_api_url=None, return_http_code=None, return_status=None, return_error_messages=None,
           split_errors=False):
    """This function creates a new group hub within a Khoros Community environment.

    .. versionadded:: 2.6.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param group_id: The unique identifier (i.e. ``id`` field) for the new group hub **(Required)**
    :type group_id: str, int
    :param group_title: The title of the group hub **(Required)**
    :type group_title: str
    :param description: A brief description of the group hub
    :type description: str, None
    :param membership_type: The ``membership_type`` value (``open``, ``closed`` or ``closed_hidden``)
    :type membership_type: dict, None
    :param open_group: Defines the group hub as an open group
    :type open_group: bool, None
    :param closed_group: Defines the group hub as a closed group
    :type closed_group: bool, None
    :param hidden_group: Defines the group hub as a closed and hidden group
    :type hidden_group: bool, None
    :param discussion_styles: A list of discussion styles that will be permitted in the group hub
    :type discussion_styles: list, None
    :param enable_blog: Defines that the **blog** discussion style should be enabled for the group hub
    :type enable_blog: bool, None
    :param enable_contest: Defines that the **contest** discussion style should be enabled for the group hub
    :type enable_contest: bool, None
    :param enable_forum: Defines that the **forum** discussion style should be enabled for the group hub
    :type enable_forum: bool, None
    :param enable_idea: Defines that the **idea** discussion style should be enabled for the group hub
    :type enable_idea: bool, None
    :param enable_qanda: Defines that the **Q&A** (``qanda``) discussion style should be enabled for the group hub
    :type enable_qanda: bool, None
    :param enable_tkb: Defines that the **TKB** (``tkb``) discussion style should be enabled for the group hub
    :type enable_tkb: bool, None
    :param all_styles_default: Defines that all discussion styles should be enabled if not otherwise specified
    :type all_styles_default: bool
    :param parent_category_id: The parent category identifier (if applicable)
    :type parent_category_id: str, int, None
    :param avatar_image_path: The file path to the avatar image to be uploaded (if applicable)
    :type avatar_image_path: str, None
    :param full_response: Determines whether the full, raw API response should be returned by the function

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``,
                                       ``return_http_code``, ``return_status`` and ``return_error_messages`` arguments.

    :type full_response: bool, None
    :param return_id: Determines if the **ID** of the new group hub should be returned by the function
    :type return_id: bool, None
    :param return_url: Determines if the **URL** of the new group hub should be returned by the function
    :type return_url: bool, None
    :param return_api_url: Determines if the **API URL** of the new group hub should be returned by the function
    :type return_api_url: bool, None
    :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by the function
    :type return_http_code: bool, None
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if any error messages associated with the API response should be
                                  returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :returns: Boolean value indicating a successful outcome (default), the full API response or one or more specific
              fields defined by function arguments
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    payload = structure_payload(khoros_object, group_id, group_title, description, membership_type, open_group,
                                closed_group, hidden_group, discussion_styles, enable_blog, enable_contest,
                                enable_forum, enable_idea, enable_qanda, enable_tkb, all_styles_default,
                                parent_category_id)
    api_url = f"{khoros_object.core['v2_base']}/grouphubs"
    if avatar_image_path:
        response = _create_group_hub_with_avatar(khoros_object, api_url, payload, avatar_image_path)
    else:
        response = _create_group_hub_without_avatar(khoros_object, api_url, payload)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors)


def _create_group_hub_with_avatar(_khoros_object, _api_url, _payload, _avatar_image_path):
    """This function creates a group hub with both a JSON payload and an image file to use as its avatar.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _api_url: The API URL to utilize in the API request
    :type _api_url: str
    :param _payload: The JSON payload to be used in the API request
    :type _payload: dict
    :param _avatar_image_path: The file path to the avatar image to be uploaded (if applicable)
    :type _avatar_image_path: str
    :returns: The API response from the multipart POST request
    :raises: :py:exc:`FileNotFoundError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    _headers = {'content-type': 'application/x-www-form-urlencoded'}
    _full_payload = api.combine_json_and_avatar_payload(_payload, _avatar_image_path)
    response = api.post_request_with_retries(_api_url, _full_payload, khoros_object=_khoros_object, multipart=True)
    return response


def _create_group_hub_without_avatar(_khoros_object, _api_url, _payload):
    """This function creates a group hub with only a JSON payload and no avatar image.

    .. versionadded:: 2.6.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _api_url: The API URL to utilize in the API request
    :type _api_url: str
    :param _payload: The JSON payload to be used in the API request
    :type _payload: dict
    :returns: The API response from the POST request
    :raises: :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    _headers = {'content-type': 'application/json'}
    _response = api.post_request_with_retries(_api_url, _payload, khoros_object=_khoros_object, headers=_headers)
    return _response


def structure_payload(khoros_object, group_id, group_title, description=None, membership_type=None, open_group=None,
                      closed_group=None, hidden_group=None, discussion_styles=None, enable_blog=None,
                      enable_contest=None, enable_forum=None, enable_idea=None, enable_qanda=None, enable_tkb=None,
                      all_styles_default=True, parent_category_id=None):
    """This function structures the payload to use in a Group Hub API request.

    .. versionadded:: 2.6.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param group_id: The unique identifier (i.e. ``id`` field) for the new group hub **(Required)**
    :type group_id: str, int
    :param group_title: The title of the group hub **(Required)**
    :type group_title: str
    :param description: A brief description of the group hub
    :type description: str, None
    :param membership_type: The ``membership_type`` value (``open``, ``closed`` or ``closed_hidden``)
    :type membership_type: dict, None
    :param open_group: Defines the group hub as an open group
    :type open_group: bool, None
    :param closed_group: Defines the group hub as a closed group
    :type closed_group: bool, None
    :param hidden_group: Defines the group hub as a closed and hidden group
    :type hidden_group: bool, None
    :param discussion_styles: A list of discussion styles that will be permitted in the group hub
    :type discussion_styles: list, None
    :param enable_blog: Defines that the **blog** discussion style should be enabled for the group hub
    :type enable_blog: bool, None
    :param enable_contest: Defines that the **contest** discussion style should be enabled for the group hub
    :type enable_contest: bool, None
    :param enable_forum: Defines that the **forum** discussion style should be enabled for the group hub
    :type enable_forum: bool, None
    :param enable_idea: Defines that the **idea** discussion style should be enabled for the group hub
    :type enable_idea: bool, None
    :param enable_qanda: Defines that the **Q&A** (``qanda``) discussion style should be enabled for the group hub
    :type enable_qanda: bool, None
    :param enable_tkb: Defines that the **TKB** (``tkb``) discussion style should be enabled for the group hub
    :type enable_tkb: bool, None
    :param all_styles_default: Defines that all discussion styles should be enabled if not otherwise specified
    :type all_styles_default: bool
    :param parent_category_id: The parent category identifier (if applicable)
    :type parent_category_id: str, int, None
    :returns: The properly formatted payload for the API request
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`
    """
    payload = {"grouphub": ""}
    required_error_msg = "The 'group_id', 'group_title' and 'membership_type' fields are required " \
                         "to create a group hub."
    if any((khoros_object, group_id, group_title, membership_type)):
        raise errors.exceptions.MissingRequiredDataError(required_error_msg)
    payload = _structure_simple_string_fields(payload, group_id, group_title, description)
    payload = _structure_membership_type(payload, membership_type, open_group, closed_group, hidden_group)
    payload = _structure_discussion_styles(payload, discussion_styles, enable_blog, enable_contest, enable_forum,
                                           enable_idea, enable_qanda, enable_tkb, all_styles_default)
    payload = _structure_parent_category(payload, parent_category_id)
    return payload


def _structure_simple_string_fields(_payload, _group_id, _group_title, _description=None):
    """This function populates the payload with the group hub ID, title and description.

    .. versionadded:: 2.6.0

    :param _payload: The payload for a Group Hub API call
    :type _payload: dict
    :param _group_id: The unique identifier (ID) of the group hub
    :type _group_id: str
    :param _group_title: The title of the group hub
    :type _group_title: str
    :param _description: A brief description of the group hub
    :type _description: str, None
    :returns: The payload with the additional fields
    """
    _payload['grouphub']['id'] = str(_group_id)
    _payload['grouphub']['title'] = str(_group_title)
    if _description:
        _payload['grouphub']['description'] = _description
    return _payload


def _structure_membership_type(_payload, _membership_type, _open_group, _closed_group, _hidden_group):
    """This function populates the payload with the ``membership_type`` data.

    .. versionadded:: 2.6.0

    :param _payload: The payload for a Group Hub API call
    :type _payload: dict
    :param _membership_type: The ``membership_type`` value (``open``, ``closed`` or ``closed_hidden``)
    :type _membership_type: dict, None
    :param _open_group: Defines the group hub as an open group
    :type _open_group: bool, None
    :param _closed_group: Defines the group hub as a closed group
    :type _closed_group: bool, None
    :param _hidden_group: Defines the group hub as a closed and hidden group
    :type _hidden_group: bool, None
    :returns: The payload with the populated ``membership_type`` field
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    _valid_membership_types = ['open', 'closed', 'closed_hidden']
    _required_msg = "The membership type must be defined when creating a new group hub."
    if not any((_open_group, _closed_group, _hidden_group)) and _membership_type not in _valid_membership_types:
        raise errors.exceptions.MissingRequiredDataError(_required_msg)
    elif _membership_type and (_membership_type in _valid_membership_types):
        _payload['grouphub']['membership_type'] = _membership_type
    else:
        _types_and_values = {'open': _open_group, 'closed': _closed_group, 'closed_hidden': _hidden_group}
        for _type, _value in _types_and_values.items():
            if _value:
                _payload['grouphub']['membership_type'] = _type
                break
    return _payload


def _structure_discussion_styles(_payload, _discussion_styles=None, _enable_blog=None, _enable_contest=None,
                                 _enable_forum=None, _enable_idea=None, _enable_qanda=None, _enable_tkb=None,
                                 _all_styles_default=True):
    """This function defines the permitted discussion styles within the payload of a group hub API request.

    .. versionadded:: 2.6.0

    :param _payload: The payload to which the information should be added
    :type _payload: dict
    :param _discussion_styles: A list of discussion styles that will be permitted in the group hub
    :type _discussion_styles: list, None
    :param _enable_blog: Defines that the **blog** discussion style should be enabled for the group hub
    :type _enable_blog: bool, None
    :param _enable_contest: Defines that the **contest** discussion style should be enabled for the group hub
    :type _enable_contest: bool, None
    :param _enable_forum: Defines that the **forum** discussion style should be enabled for the group hub
    :type _enable_forum: bool, None
    :param _enable_idea: Defines that the **idea** discussion style should be enabled for the group hub
    :type _enable_idea: bool, None
    :param _enable_qanda: Defines that the **Q&A** (``qanda``) discussion style should be enabled for the group hub
    :type _enable_qanda: bool, None
    :param _enable_tkb: Defines that the **TKB** (``tkb``) discussion style should be enabled for the group hub
    :type _enable_tkb: bool, None
    :param _all_styles_default: Defines that all discussion styles should be enabled if not otherwise specified
    :type _all_styles_default: bool
    :returns: The payload with the included ``conversation_styles`` field and value(s)
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`
    """
    _required_msg = "At least one discussion style must be defined when creating a new group hub."
    if not any((_discussion_styles, _enable_blog, _enable_contest, _enable_forum, _enable_idea, _enable_qanda,
                _enable_tkb)):
        if _all_styles_default:
            _discussion_styles = VALID_DISCUSSION_STYLES
        else:
            raise errors.exceptions.MissingRequiredDataError(_required_msg)
    if _discussion_styles:
        if isinstance(_discussion_styles, str):
            _discussion_styles = [_discussion_styles]
        elif not isinstance(_discussion_styles, list):
            raise errors.exceptions.InvalidPayloadValueError(value=_discussion_styles, field='conversation_styles')
        for _style in _discussion_styles:
            if _style not in VALID_DISCUSSION_STYLES:
                raise errors.exceptions.InvalidPayloadValueError(value=_style, field='conversation_styles')
        _payload['grouphub']['conversation_styles'] = _discussion_styles
    else:
        _discussion_styles = []
        _discussion_toggles = {
            'blog': _enable_blog,
            'contest': _enable_contest,
            'forum': _enable_forum,
            'idea': _enable_idea,
            'qanda': _enable_qanda,
            'tkb': _enable_tkb
        }
        for _value, _toggle in _discussion_toggles.items():
            if _toggle:
                _discussion_styles.append(_value)
        _payload['grouphub']['conversation_styles'] = _discussion_styles
    return _payload


def _structure_parent_category(_payload, _parent_id):
    """This function structures the parent category field for a group hub if applicable.

    .. versionadded:: 2.6.0

    :param _payload: The payload to which the parent category field should be added
    :type _payload: dict
    :param _parent_id: The parent category identifier
    :type _parent_id: int, str, None
    :returns: The payload with the added field if applicable
    """
    if _parent_id:
        _parent_dict = {'id': str(_parent_id)}
        _payload['grouphub']['parent_category'] = _parent_dict
    return _payload


