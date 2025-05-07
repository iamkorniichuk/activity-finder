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


class WithinTransform(models.Transform):
    lookup_name = "within"
    output_field = models.BooleanField()

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)

        sql = f"{lhs}[1] <= {rhs_sql} AND {rhs_sql} < {lhs}[2]"
        return sql, params + rhs_params
