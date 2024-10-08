from components.coffeedb import Cluster

cluster = Cluster('data')
db = cluster['gestor_finanzas']

usuario = db['usuario']
gasto = db['gasto']
ingreso = db['ingreso']
categoria = db['categoria']

usuario.create_index('username')