def object_id_to_str(collection={}, many=False):
    """
        recibe una documento o lista de documentos, en caso de tener una
        llave '_id' se convertira en string y retornara documento o lista
        de documentos
    """
    if many:
        result = []
        for document in collection:
            if '_id' in document:
                document['_id'] = str(document['_id'])
            result.append(document)
        return result
    if '_id' in collection:
        collection['_id'] = str(collection['_id'])
    return collection


def remove_object_id(collection={}, many=False):
    """
        remueve la llave '_id' de un diccionario
    """
    if many:
        for document in collection:
            document.pop('_id', None)
        return collection
    collection.pop('_id', None)
    return collection
