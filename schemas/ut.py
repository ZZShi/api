from datetime import datetime

from fastapi import Query
from pydantic import BaseModel

from common.resp import ORMModel


class TaskUpdate(BaseModel):
    task_name: str
    task_type: str
    crontab: str
    content: dict
    case_path: list
    is_multi_progress: bool
    process_num: int
    group: str


class TaskCreate(TaskUpdate):
    ...


class TaskInfo(ORMModel):
    task_name: str
    task_type: str
    crontab: str
    content: dict
    case_path: list
    is_multi_progress: bool
    process_num: int
    group: str


class HistoryInfo(ORMModel):
    report_url: str
    report_name: str
    status: str
    failed: int
    broken: int
    skipped: int
    passed: int
    unknown: int
    total: int


class DetailInfo(ORMModel):
    epic: str
    feature: str
    story: str
    func: str
    severity: str
    status: str
    start_time: datetime
    stop_time: datetime
    duration: str
    parameters: str
    failed_reason: str
    developer: str
    test_developer: str
    order: int
    case_url: str


def task_filter(task_name: str = Query(None), task_type: int = Query(None)):
    query = {}
    if task_name:
        query.setdefault("task_name__icontains", task_name)
    if task_type:
        query.setdefault("task_type", task_type)
    return query


def history_filter(report_name: str = Query(None), status: str = Query(None)):
    query = {}
    if report_name:
        query.setdefault("report_name__icontains", report_name)
    if status:
        query.setdefault("status", status)
    return query


def detail_filter(pk: str = Query(None, alias="id"), epic: str = Query(None),
                  feature: str = Query(None), story: str = Query(None),
                  status: str = Query(None), developer: str = Query(None),
                  test_developer: str = Query(None)):
    query = {}
    if pk:
        query.setdefault("id", pk)
    if epic:
        query.setdefault("epic", epic)
    if feature:
        query.setdefault("feature", feature)
    if story:
        query.setdefault("story", story)
    if status:
        query.setdefault("status", status)
    if developer:
        query.setdefault("developer__icontains", developer)
    if test_developer:
        query.setdefault("test_developer__icontains", test_developer)
    return query
