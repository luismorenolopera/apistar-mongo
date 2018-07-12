def object_id_to_str(collection={}, many=False):
    if many:
        result = []
        for document in collection:
            document['_id'] = str(document['_id'])
            result.append(document)
        return result
    collection['_id'] = str(collection['_id'])
    return collection


def remove_object_id(collection={}, many=False):
    if many:
        for document in collection:
            document.pop('_id', None)
        return collection
    collection.pop('_id', None)
    return collection
