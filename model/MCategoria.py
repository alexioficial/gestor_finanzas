from model.MMain import categoria

def RegCategoria(nombre, status):
    return categoria.insert({'nombre': nombre, 'status': status})

def UCategoria(idcategoria, nombre, status):
    return categoria.update({'_uuid_': idcategoria}, {'$set': {'nombre': nombre, 'status': status}})

def SCategorias():
    return categoria.select()

def SCategoriasActivas():
    return categoria.select({'status': 'A'})

def SCategoriasNombre(nombre):
    return categoria.select({'nombre': nombre})