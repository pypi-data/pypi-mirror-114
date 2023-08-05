from enum import Enum, unique


@unique
class ReturnStatus(Enum):
    CANNOT_ROTATE = "CANNOT_ROTATE"
    HAND_IS_FULL = "HAND_IS_FULL"
    IS_CLOSED_COMPLETELY = "IS_CLOSED_COMPLETELY"
    IS_OPENED_COMPLETELY = "IS_OPENED_COMPLETELY"
    NOT_HELD = "NOT_HELD"
    NOT_INTERACTABLE = "NOT_INTERACTABLE"
    NOT_MOVEABLE = "NOT_MOVEABLE"
    NOT_OBJECT = "NOT_OBJECT"
    NOT_OPENABLE = "NOT_OPENABLE"
    NOT_RECEPTACLE = "NOT_RECEPTACLE"
    NOT_PICKUPABLE = "NOT_PICKUPABLE"
    OBSTRUCTED = "OBSTRUCTED"
    OUT_OF_REACH = "OUT_OF_REACH"
    SUCCESSFUL = "SUCCESSFUL"
    SUCCESSFUL_WITH_INVALID_PARAMETERS = "SUCCESSFUL_WITH_INVALID_PARAMETERS"
    UNDEFINED = "UNDEFINED"
    WRONG_POSE = "WRONG_POSE"
    FAILED = "FAILED"
