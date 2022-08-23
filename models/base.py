from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True


class Event(TimestampMixin):
    name = fields.TextField()
    age = fields.IntField()

    class Meta:
        table = "event"

    def __str__(self):
        return self.name


class UtTask(TimestampMixin):
    TaskType = (
        (0, '定时任务'),
        (1, '临时任务'),
    )
    task_name = fields.CharField(null=True, max_length=32, description='任务名称')
    task_type = fields.CharField(null=True, max_length=1, choice=TaskType, description='任务类型')
    crontab = fields.CharField(null=True, max_length=16, default="0 0 0 0 0 0 0", description='Corntab 表达式')
    content = fields.JSONField(null=True, description='选择的 case')
    case_path = fields.JSONField(null=True, description='用例路径')
    is_multi_progress = fields.BooleanField(null=False, default=False, description='是否多进程')
    process_num = fields.IntField(null=True, max_length=8, description='进程数')
    group = fields.CharField(null=True, max_length=32, description='分组方式')

    class Meta:
        ordering = ["-id"]
        table_description = "自动化任务"
        table = "uttask"
