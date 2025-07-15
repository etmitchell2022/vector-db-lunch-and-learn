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


class MovieSearchResultSchema(MovieSchema):
    document = fields.Str()
    embedding = fields.List(fields.Float())


class CoordinatesSchema(Schema):
    x = fields.Float()
    y = fields.Float()


class MovieVectorVisualizationSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    overview = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    popularity = fields.Float()
    language = fields.Str()
    poster_path = fields.Str()
    document = fields.Str()
    embedding = fields.List(fields.Float())
    similarity = fields.Float()
    raw_similarity = fields.Float()
    coordinates = fields.Nested(CoordinatesSchema)


class MovieSearchArgs(Schema):
    search = fields.Str(required=True)
