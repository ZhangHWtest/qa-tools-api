#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.interface import server
from env import SERVER_PORT

server.run(
    host='0.0.0.0',
    port=SERVER_PORT,
    debug=True
)
