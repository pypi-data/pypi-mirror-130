#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Tradologics Python SDK
# https://tradologics.com
#
# Copyright Tradologics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import requests

_SANDBOX_URL = "https://api.tradologics.com/v1/sandbox"
_TOKEN = None


def set_token(token):
    global _TOKEN
    _TOKEN = f'Bearer {token}'


def tradehook(kind: str, strategy: callable, **kwargs):
    """
    authorization required

    Parameters
    ----------
    kind : available kinds: ["bar", "order", "order_{YOUR_STATUS}  (example: "order_filled")", "position",
    "position_expire", "price", "price_expire", "error"]
    strategy : callback
    kwargs : payload

    Returns
    -------
    json obj
    """

    url = f'{_SANDBOX_URL}/{kind.replace("_", "/")}'
    headers = {'Authorization': _TOKEN}
    result = requests.get(url, data=json.dumps(kwargs), headers=headers)
    strategy(kind.split('_')[0], result.json())
