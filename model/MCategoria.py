from components.conexion import categoria, GenerarUUID

def RegCategoria(idusuario, nombre, status: bool, tipo):
    return categoria.insert_one({
        'idcategoria': GenerarUUID(), 
        'nombre': nombre, 
        'status': 'A' if status else 'I', 
        'tipo': tipo,
        'idusuario': idusuario
    })

def UCategoria(idusuario, idcategoria, nombre, status: bool, tipo):
    return categoria.update_one(
        {'idusuario': idusuario, 'idcategoria': idcategoria}, 
        {'$set': {'nombre': nombre, 'status': 'A' if status else 'I', 'tipo': tipo}}
    )

def SCategorias(idusuario):
    return list(categoria.find({'idusuario': idusuario}))

def SCategoriasActivas(idusuario):
    return list(categoria.find({'idusuario': idusuario, 'status': 'A'}))

def SCategoriasNombre(idusuario, nombre):
    return categoria.find_one({'idusuario': idusuario, 'nombre': nombre})

def DCategoria(idusuario, idcategoria):
    return categoria.delete_one({'idusuario': idusuario, 'idcategoria': idcategoria})

def SCategoriasPorTipo(idusuario, tipo):
    return list(categoria.find({'idusuario': idusuario, 'tipo': tipo, 'status': 'A'}))