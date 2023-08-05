from enum import Enum
from datetime import datetime


class TypeEnum(Enum):
    CALL = "call"
    SMS = "sms"


class AlertCOM:
    id_alert_communication: int
    phone: str
    id_org: int
    id_rule: int
    type: TypeEnum
    created_at: datetime
    updated_at: datetime

    def __init__(self, id_alert_communication: int, phone: str, id_org: int, id_rule: int, type: TypeEnum, created_at: datetime, updated_at: datetime) -> None:
        self.id_alert_communication = id_alert_communication
        self.phone = phone
        self.id_org = id_org
        self.id_rule = id_rule
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at


class AlertRuleData:
    alert_com: AlertCOM

    def __init__(self, alert_com) -> None:
        self.alert_com = AlertCOM(**dict(alert_com))
