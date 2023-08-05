from enum import IntEnum
from re import match
from typing import Dict, Any, Optional, Union, List

from robotnikmq import Topic, Message, RobotnikConfig
from typeguard import typechecked


@typechecked
class Priority(IntEnum):
    INFO = 0
    ACTIVITY = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


INFO = {'info', 'information', 'i'}
ACTIVITY = {'activity', 'a'}
WARNING = {'warning', 'warn', 'w'}
ERROR = {'error', 'err', 'e'}
CRITICAL = {'critical', 'crit', 'c'}


@typechecked
def priority_of(candidate: str) -> Priority:
    if candidate.lower() in INFO:
        return Priority.INFO
    if candidate.lower() in ACTIVITY:
        return Priority.ACTIVITY
    if candidate.lower() in WARNING:
        return Priority.WARNING
    if candidate.lower() in ERROR:
        return Priority.ERROR
    if candidate.lower() in CRITICAL:
        return Priority.CRITICAL
    raise ValueError(f'"{candidate}" cannot be mapped to a valid priority')


class NotificationMsg:
    @typechecked
    def __init__(self,
                 contents: Dict[str, Any],
                 alert_key: Union[str, List[str], None] = None,
                 desc: Optional[str] = None,
                 ttl: Optional[int] = None,
                 priority: Optional[Priority] = None):
        self.contents = contents
        self.alert_key = '['+']['.join(alert_key)+']' if isinstance(alert_key, List) else alert_key
        self.desc = desc
        self.ttl = ttl
        self.priority = priority or Priority.INFO

    @typechecked
    def broadcast(self, exchange: str, route: str, config: Optional[RobotnikConfig] = None) -> None:
        broadcast_msg(exchange, route, self, config)


@typechecked
class InfoMsg(NotificationMsg):
    def __init__(self,
                 contents: Dict[str, Any],
                 ttl: Optional[int] = None):
        super().__init__(contents=contents, ttl=ttl, priority=Priority.INFO)


@typechecked
class ActivityMsg(NotificationMsg):
    def __init__(self,
                 contents: Dict[str, Any],
                 ttl: Optional[int] = None):
        super().__init__(contents=contents, ttl=ttl, priority=Priority.ACTIVITY)


class AlertComparison:
    @typechecked
    def __init__(self, first: 'AlertMsg', second: 'AlertMsg'):
        self.key = first.key, second.key
        self.desc = first.desc, second.desc
        self.ttl = first.ttl, second.ttl
        self.priority = first.priority, second.priority
        self.contents = first.contents, second.contents

    @property
    def key_equal(self) -> bool:
        return self.key[0] == self.key[1]

    @property
    def desc_equal(self) -> bool:
        return self.desc[0] == self.desc[1]

    @property
    def ttl_equal(self) -> bool:
        return self.ttl[0] == self.ttl[1]

    @property
    def priority_equal(self) -> bool:
        return self.priority[0] == self.priority[1]

    @property
    def key_match(self) -> bool:
        return bool(match(*self.key) or match(self.key[1], self.key[0]))

    @property
    def desc_match(self) -> bool:
        return bool(match(*self.desc) or match(self.desc[1], self.desc[0]))


class AlertMsg(NotificationMsg):
    @typechecked
    def __init__(self,
                 contents: Dict[str, Any],
                 key: Union[str, List[str]],
                 desc: str,
                 ttl: Optional[int] = None,
                 priority: Priority = None):
        if priority is not None and priority < Priority.WARNING:
            raise ValueError('Alerts can only have a priority of WARNING (2) or higher')
        if not desc:
            raise ValueError('Alerts have to have a description')
        if not key:
            raise ValueError('Alerts have to have a key')
        super().__init__(alert_key=key, desc=desc, priority=priority or Priority.WARNING,
                         ttl=ttl or 30, contents=contents)
        self.desc: str = desc
        self.ttl: int = ttl or 30
        self.priority: Priority = priority or Priority.WARNING
        self.alert_key: str = '['+']['.join(key)+']' if isinstance(key, List) else key

    @typechecked
    def compare(self, other: 'AlertMsg') -> AlertComparison:
        return AlertComparison(self, other)

    @property
    def key(self) -> str:
        return self.alert_key

    @property
    def description(self) -> Optional[str]:
        return self.desc


class WarningMsg(AlertMsg):
    @typechecked
    def __init__(self,
                 contents: Dict[str, Any],
                 key: Union[str, List[str]],
                 desc: str,
                 ttl: Optional[int] = None):
        if not desc:
            raise ValueError('Warnings (alerts) have to have a description')
        if not key:
            raise ValueError('Warnings (alerts) have to have a key')
        super().__init__(key=key, desc=desc, priority=Priority.WARNING,
                         ttl=ttl or 30, contents=contents)


class ErrorMsg(AlertMsg):
    @typechecked
    def __init__(self,
                 contents: Dict[str, Any],
                 key: Union[str, List[str]],
                 desc: str,
                 ttl: Optional[int] = None):
        if not desc:
            raise ValueError('Errors (alerts) have to have a description')
        if not key:
            raise ValueError('Errors (alerts) have to have a key')
        super().__init__(key=key, desc=desc, priority=Priority.ERROR,
                         ttl=ttl or 30, contents=contents)


class CriticalMsg(AlertMsg):
    @typechecked
    def __init__(self,
                 contents: Dict[str, Any],
                 key: Union[str, List[str]],
                 desc: str,
                 ttl: Optional[int] = None):
        if not desc:
            raise ValueError('Critical Alerts have to have a description')
        if not key:
            raise ValueError('Critical Alerts have to have a key')
        super().__init__(key=key, desc=desc, priority=Priority.CRITICAL,
                         ttl=ttl or 30, contents=contents)


@typechecked
def broadcast_msg(exchange: str, route: str, notification: NotificationMsg,
                  config: Optional[RobotnikConfig] = None) -> None:
    broadcast(exchange=exchange,
              route=route,
              priority=notification.priority,
              contents=notification.contents,
              ttl=notification.ttl,
              description=notification.desc,
              alert_key=notification.alert_key,
              config=config)


@typechecked
def broadcast_alert_msg(exchange: str, route: str, alert: AlertMsg,
                        config: Optional[RobotnikConfig] = None) -> None:
    broadcast(exchange=exchange,
              route=route,
              priority=alert.priority,
              contents=alert.contents,
              ttl=alert.ttl,
              description=alert.desc,
              alert_key=alert.alert_key,
              config=config)


@typechecked
def broadcast(exchange: str,
              route: str,
              priority: Priority,
              contents: Dict[str, Any],
              ttl: Optional[int] = None,
              description: Optional[str] = None,
              alert_key: Optional[str] = None,
              config: Optional[RobotnikConfig] = None):
    _contents: Dict[str, Any] = {'priority': priority.value}
    if priority.value >= 2:
        assert description is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have a description'
        assert ttl is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have a ttl (to clear an alert, set the ttl to 0)'
        assert alert_key is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have an alert_key'
    if ttl is not None:
        _contents['ttl'] = ttl
    if description is not None:
        _contents['description'] = description
    if alert_key is not None:
        _contents['alert_key'] = alert_key
    _contents.update(contents)
    route += f'.{priority.name.lower()}'
    Topic(exchange=exchange, config=config).broadcast(Message(contents=_contents),
                                                      routing_key=route)


@typechecked
def broadcast_info(exchange: str, route: str, contents: Dict[str, Any],
                   config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, priority=Priority.INFO, contents=contents, config=config)


@typechecked
def broadcast_activity(exchange: str, route: str, contents: Dict[str, Any],
                       config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, priority=Priority.ACTIVITY, contents=contents, config=config)


@typechecked
def broadcast_alert(exchange: str,
                    route: str,
                    description: str,
                    alert_key: str,
                    contents: Dict[str, Any],
                    ttl: int = 30,
                    priority: Priority = Priority.WARNING,
                    config: Optional[RobotnikConfig] = None) -> None:
    broadcast(exchange, route, ttl=ttl, priority=priority, contents=contents,
              config=config, description=description, alert_key=alert_key)


@typechecked
def broadcast_warning(exchange: str, route: str, desc: str, alert_key: str,
                      contents: Dict[str, Any], ttl: int = 30,
                      config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.WARNING, config=config)


@typechecked
def broadcast_error(exchange: str, route: str, desc: str, alert_key: str,
                    contents: Dict[str, Any], ttl: int = 30,
                    config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.ERROR, config=config)


@typechecked
def broadcast_critical(exchange: str, route: str, desc: str, alert_key: str,
                       contents: Dict[str, Any], ttl: int = 30,
                       config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.CRITICAL, config=config)
