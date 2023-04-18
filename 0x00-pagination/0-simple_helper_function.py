#!/usr/bin/env python3
''' Simple helper function '''
from typing import Tuple


def index_range(page_size: int, page: int) -> Tuple[int, int]:
    ''' Def index range '''
    index = page * page_size - page_size
    index_1 = index + page_size
    return (index, index_1)
