""" bot states for conversation handler """
from enum import Enum


class States(Enum):
    """ states keys """

    MENU = 0

    SCHEDULE = 2
    ACCOUNT = 3
    TIMER = 15

    REGISTRATION = "reg"  # return request
    NEXT = "next"  # next handler
    BACK = "back"  # previous handler
    ROLLBACK = "rollback"  # previous handler with another msg
    DOUBLENEXT = "doublenext"  # jump to the next handler

    ADMIN_MENU = 10
    PUSH = 13
    AD = 16
