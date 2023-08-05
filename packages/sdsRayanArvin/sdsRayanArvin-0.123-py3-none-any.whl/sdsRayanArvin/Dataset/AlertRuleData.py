from enum import Enum
from datetime import datetime


class TypeEnum(Enum):
    CALL = "call"
    SMS = "sms"


class AlertCOM:
    ID_alert_communication: int
    phone: str
    ID_org: int
    ID_rule: int
    type: TypeEnum
    created_at: datetime
    updated_at: datetime

    def __init__(self, ID_alert_communication: int, phone: str, ID_org: int, ID_rule: int, type: TypeEnum, created_at: datetime, updated_at: datetime) -> None:
        self.ID_alert_communication = ID_alert_communication
        self.phone = phone
        self.ID_org = ID_org
        self.ID_rule = ID_rule
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at


class AlertRuleData:
    alert_com: AlertCOM

    def __init__(self, alert_com) -> None:
        self.alert_com = AlertCOM(**dict(alert_com))
