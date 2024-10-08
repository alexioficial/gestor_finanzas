from model.MMain import categoria

def RegCategoria(nombre):
    return categoria.insert({'nombre': nombre, 'status': 'A'})

def UCategoria(idcategoria, nombre, status):
    return categoria.update({'_uuid_': idcategoria}, {'$set': {'nombre': nombre, 'status': status}})

def SCategorias():
    return categoria.select()

def SCategoriasActivas():
    return categoria.select({'status': 'A'})