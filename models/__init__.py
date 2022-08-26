import datetime
from tortoise import fields


class DatetimeField(fields.DatetimeField):
    """重载日期时间模型字段"""

    def __init__(self, *args, **kwargs):
        super(DatetimeField, self).__init__(*args, **kwargs)

    def to_python_value(self, value: datetime.datetime) -> [str, None]:
        if value is None:
            value = None
        else:
            try:
                value = value.strftime("%Y-%m-%d %H:%M:%S")
                self.validate(value)
            except Exception as ex:
                value = super(DatetimeField, self).to_python_value(value)
        return value


fields.DatetimeField = DatetimeField
