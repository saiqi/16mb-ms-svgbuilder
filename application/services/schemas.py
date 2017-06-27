from marshmallow import Schema, fields, post_load

from application.services.reports.player_news_report import PlayerNewsReport


class SeasonInformationSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)


class SeasonSchema(Schema):
    id = fields.Str(required=True)
    type = fields.Str()
    provider = fields.Str()
    common_name = fields.Str(required=True)
    informations = fields.Nested(SeasonInformationSchema)


class PlayerInformationSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    nickname = fields.Str(allow_none=True)


class PlayerSchema(Schema):
    id = fields.Str(required=True)
    type = fields.Str()
    provider = fields.Str()
    common_name = fields.Str(required=True)
    informations = fields.Nested(PlayerInformationSchema)


class PlayerDNASchema(Schema):
    offensive = fields.Float(required=True)
    versatility = fields.Float(required=True)
    playermaker = fields.Float(required=True)


class PlayerPositionSchema(Schema):
    defensive_expert = fields.Float(required=True)
    defensive_versatile = fields.Float(required=True)
    offensive_expert = fields.Float(required=True)
    offensive_versatile = fields.Float(required=True)


class PlayerSummarySchema(Schema):
    type = fields.Str(required=True)
    name = fields.Str(required=True)
    value = fields.Int(required=True)


class PlayerEventSchema(Schema):
    type = fields.Str(required=True)
    name = fields.Str(required=True)
    value = fields.Int(required=True)


class PlayerStatsSchema(Schema):
    formula_id = fields.Str(required=True)
    name = fields.Str(required=True)
    from_date = fields.Str()
    to_date = fields.Str()
    interval = fields.Float(required=True)
    is_negative = fields.Bool()
    is_success_rate = fields.Bool()
    numerator = fields.Float(allow_none=True)
    denominator = fields.Float(allow_none=True)
    value = fields.Float(required=True)
    rank = fields.Int(required=True)
    player_id = fields.Str(required=True)


class PlayerNewsReportSchema(Schema):
    title = fields.Str()
    background = fields.Str(allow_none=True)
    player_picture = fields.Str(allow_none=True)
    season_picture = fields.Str(allow_none=True)
    competition_picture = fields.Str(allow_none=True)
    season_entity = fields.Nested(SeasonSchema, required=True)
    player_entity = fields.Nested(PlayerSchema, required=True)
    summary = fields.List(fields.Nested(PlayerSummarySchema))
    events = fields.List(fields.Nested(PlayerEventSchema))
    stats = fields.List(fields.Nested(PlayerStatsSchema), required=True)

    @post_load
    def make_report(self, data):
        return PlayerNewsReport(**data)
