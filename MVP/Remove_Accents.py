#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 20:01:12 2020

@author: andrew
"""

import unicodedata

def remove_accents(input_str):

    if type(input_str) == unicode:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    else:
        return input_str