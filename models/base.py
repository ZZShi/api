from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        ordering = ["-id"]
        abstract = True


class Events(TimestampMixin):
    name = fields.TextField()
    age = fields.IntField()
    x = fields.TextField()

    class Meta:
        table = "events"

    def __str__(self):
        return self.name


class UtTasks(TimestampMixin):
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
        table_description = "自动化任务"
        table = "ut_tasks"

    def __str__(self):
        return self.task_name


class UtHistories(TimestampMixin):
    """
    测试报告历史数据
    """
    Status = (
        (0, '未知状态'),
        (1, '未开始'),
        (2, '运行中'),
        (3, '运行成功'),
        (4, '运行失败'),
        (5, '停止运行')
    )

    report_url = fields.CharField(null=True, max_length=128, description="报告链接")
    report_name = fields.CharField(null=True, max_length=128, description="报告名称")
    status = fields.CharField(null=True, max_length=1, choices=Status, default=0, description="状态")
    failed = fields.IntField(null=True, default=0, description="失败")
    broken = fields.IntField(null=True, default=0, description="异常")
    skipped = fields.IntField(null=True, default=0, description="跳过")
    passed = fields.IntField(null=True, default=0, description="通过")
    unknown = fields.IntField(null=True, default=0, description="未知")
    total = fields.IntField(null=True, default=0, description="总数")

    class Meta:
        table = "ut_histories"

    def __str__(self):
        return self.report_name


class UtOverviews(TimestampMixin):
    """
    测试报告概况数据
    """
    epic = fields.CharField(null=True, max_length=64, description="epic")
    feature = fields.CharField(null=True, max_length=64, description="feature")
    story = fields.CharField(null=True, max_length=64, description="story")
    failed = fields.IntField(null=True, description="未通过")
    broken = fields.IntField(null=True, description="失败")
    skipped = fields.IntField(null=True, description="跳过")
    passed = fields.IntField(null=True, description="通过")
    unknown = fields.IntField(null=True, description="未知原因")
    # order = fields.ForeignKeyField("models.base.UtHistories", related_name="id")
    order = fields.IntField(null=True, description="历史报告 ID")

    class Meta:
        table = "ut_overviews"

    def __str__(self):
        return f"{self.feature} - {self.story}"


class UtDetails(TimestampMixin):
    """
    测试报告详情数据
    """
    epic = fields.CharField(null=True, max_length=64, description="epic")
    feature = fields.CharField(null=True, max_length=64, description="feature")
    story = fields.CharField(null=True, max_length=64, description="story")
    func = fields.CharField(null=True, max_length=128, description="方法名称")
    severity = fields.CharField(null=True, max_length=32, description="用例等级")
    status = fields.CharField(null=True, max_length=32, description="状态")
    start_time = fields.DatetimeField(null=True, default=0, description="开始时间")
    stop_time = fields.DatetimeField(null=True, default=0, description="结束时间")
    duration = fields.CharField(null=True, max_length=128, description="耗时")
    parameters = fields.TextField(null=True, description="参数")
    failed_reason = fields.TextField(null=True, description="失败原因")
    developer = fields.CharField(null=True, max_length=48, description="开发同学邮箱")
    test_developer = fields.CharField(null=True, max_length=48, description="测试同学邮箱")
    # order = fields.ForeignKeyField("ut.UtHistory", related_name="id")
    order = fields.IntField(null=True, description="历史报告 ID")
    case_url = fields.CharField(null=True, max_length=128, description="用例链接")

    class Meta:
        table = "ut_details"

    def __str__(self):
        return f"{self.feature} - {self.story}"
