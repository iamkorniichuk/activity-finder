from django.db import models


class StartTransform(models.Transform):
    lookup_name = "start"
    output_field = models.TimeField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return f"{lhs}[1]", params


class EndTransform(models.Transform):
    lookup_name = "end"
    output_field = models.TimeField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return f"{lhs}[2]", params


class DurationTransform(models.Transform):
    lookup_name = "duration"
    output_field = models.DurationField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return f"{lhs}[2] - {lhs}[1]", params
