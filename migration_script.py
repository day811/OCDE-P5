import pandas as pd
import logging
import pymongo

def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total
