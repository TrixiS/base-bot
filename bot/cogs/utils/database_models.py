from tortoise import Model, fields


class CooldownBucket(Model):
    command_name = fields.TextField()
    guild_id = fields.IntField()
    member_id = fields.IntField()
    uses = fields.IntField(default=1)
    window = fields.DatetimeField(default=None, null=True)
