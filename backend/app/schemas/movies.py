from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    overview = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    popularity = fields.Float()
    language = fields.Str()
    poster_path = fields.Str()
    similarity = fields.Float()
    raw_similarity = fields.Float()


class MovieSearchArgs(Schema):
    search = fields.Str(required=True)
