#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
returns relative path from project root directory
"""

import os

def get_relative_path(file_path):
    '''

    Parameters
    ----------
    file_path : str
        absolute path of file with parent directory.

    Returns
    -------
    relative path to root directory.

    '''
    absolute_path = os.path.dirname(__file__)
    relative_path = file_path
    full_path = os.path.join(absolute_path, '..', relative_path)
    
    return full_path