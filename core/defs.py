from query_handler import MongoConnection


def MongoCursorDefs(db):
    return MongoConnection().getCursor(db)
