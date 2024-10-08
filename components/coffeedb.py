import os
import components.tools as tools
import datetime
from typing import Union
from components.results import DeleteResult, UpdateResult

class Collection:
    def __init__(self, cluster_name: str, database_name: str, name: str):
        self._cluster_name = cluster_name
        self._database_name = database_name
        self.name = name
        ruta = tools.RutaRelativa(f"{cluster_name}/{database_name}/{name}")
        self._ruta = ruta
        os.makedirs(ruta, exist_ok=True)
        ruta_config = f"{ruta}/config.json"
        self._ruta_indexes = f"{ruta}/indexes"
        if not tools.ExisteFile(ruta_config):
            tools.CrearArchivo(ruta_config, "")
            os.makedirs(self._ruta_indexes, exist_ok=True)
            configuracion = {
                'count': 0,
                'each_stack': 1000,
                'stacks': 1,
                'creation_date': tools.FechaToStr(datetime.datetime.now()),
                'indexes': []
            }
            tools.EscribirArchivoJson(ruta_config, configuracion)
        self._config = tools.CargarArchivoJson(ruta_config)
        self._ruta_config = ruta_config
        self._indexes_cache = {}  # Cache de índices en memoria

        # Cargar archivos de índices en memoria
        for index in self._config['indexes']:
            index_file_path = os.path.join(self._ruta_indexes, f"{index}.json")
            if tools.ExisteFile(index_file_path):
                self._indexes_cache[index] = tools.CargarArchivoJson(index_file_path)
            else:
                self._indexes_cache[index] = {}

        self.create_index('_uuid_')

    def stack(self, each):
        self._modificar_config('each_stack', each)

    def _reload_config(self):
        self._config = tools.CargarArchivoJson(self._ruta_config)

    def _modificar_config(self, key, value):
        data = tools.CargarArchivoJson(self._ruta_config)
        data[key] = value
        tools.EscribirArchivoJson(self._ruta_config, data)
        self._reload_config()

    def get_config(self, key):
        self._reload_config()
        return self._config.get(key)

    def create_index(self, field: str):
        if field not in self._config['indexes']:
            self._config['indexes'].append(field)
            tools.EscribirArchivoJson(self._ruta_config, self._config)

            # Crear archivo para el índice en memoria y luego disco
            index_file_path = os.path.join(self._ruta_indexes, f"{field}.json")
            if not os.path.exists(index_file_path):
                self._indexes_cache[field] = {}
                tools.EscribirArchivoJson(index_file_path, {})

    def _flush_indexes_to_disk(self):
        """Guardar todos los índices desde la cache a disco."""
        for index, data in self._indexes_cache.items():
            index_file_path = os.path.join(self._ruta_indexes, f"{index}.json")
            tools.EscribirArchivoJson(index_file_path, data)

    def insert(self, data: dict) -> Union[int, None]:
        self._reload_config()

        has_uuid = data.get('_uuid_') is None
        _uuid_ = tools.GenerarUuid()
        data = {
            **({'_uuid_': _uuid_} if has_uuid else {}),
            **data
        }

        # Verificar duplicados en índices antes de insertar, usando la cache
        for index in self._config['indexes']:
            index_value = data.get(index)
            if index_value is not None:
                if index_value in self._indexes_cache.get(index, {}):
                    print(f"Duplicate entry for index '{index}': {index_value}. Insertion skipped.")
                    return None  # No se realiza la inserción

        # Obtener configuración de stacks
        each_stack: int = self.get_config('each_stack')
        count: int = self.get_config('count')
        stacks: int = self.get_config('stacks')

        # Calcular en qué stack debe ir este archivo
        stack_id = (count // each_stack) + 1
        stack_folder = os.path.join(self._ruta, str(stack_id * each_stack))

        # Crear el stack si no existe
        if not os.path.exists(stack_folder):
            os.makedirs(stack_folder)
            stacks += 1
            self._modificar_config('stacks', stacks)

        # Guardar el archivo en el stack adecuado
        file_id = count + 1
        file_path = os.path.join(stack_folder, f"{file_id}.json")
        tools.EscribirArchivoJson(file_path, data)

        # Aumentar el contador de registros
        self._modificar_config('count', count + 1)

        # Actualizar índices en la cache
        for index in self._config['indexes']:
            index_value = data.get(index)
            if index_value is not None:
                if index_value not in self._indexes_cache[index]:
                    self._indexes_cache[index][index_value] = []
                self._indexes_cache[index][index_value].append(f"{file_id}.json")

        # Guardar índices en disco después de las inserciones
        self._flush_indexes_to_disk()

        return file_id

    def select(self, filtro=None, project=None, limit=None):
        result = []
        stacks_folders = tools.ListCarpetas(self._ruta)

        if filtro and any(key in self._config['indexes'] for key in filtro.keys()):
            # Usar índice para realizar la búsqueda
            for key, value in filtro.items():
                if key in self._config['indexes']:
                    index_data = self._indexes_cache.get(key, {})
                    if value in index_data:
                        file_ids = index_data[value]
                        for file_id in file_ids:
                            # Buscar el archivo en cada stack
                            for stack in stacks_folders:
                                stack_folder = os.path.join(self._ruta, stack)
                                file_path = os.path.join(stack_folder, file_id)
                                
                                if os.path.exists(file_path):
                                    datos = tools.CargarArchivoJson(file_path)
                                    result.append(self._project(datos, project))
                                    
                                    if limit and len(result) >= limit:
                                        return result
                return result

        # Búsqueda sin índice
        for stack in stacks_folders:
            ruta_del_stack = f"{self._ruta}/{stack}"
            archivos = tools.ListArchivos(ruta_del_stack, '.json', True)

            left = 0
            right = len(archivos) - 1
            total_count = 0

            while left <= right:
                if limit is not None and total_count >= limit:
                    break
                if left == right:
                    archivos_batch = [archivos[left]]
                else:
                    archivos_batch = [archivos[left], archivos[right]]

                for archivo in archivos_batch:
                    datos = tools.CargarArchivoJson(f"{ruta_del_stack}/{archivo}")

                    if all(datos.get(k) == v for k, v in (filtro or {}).items()):
                        result.append(self._project(datos, project))
                        total_count += 1

                left += 1
                right -= 1

            if limit is not None and total_count >= limit:
                break

        return result

    def _project(self, data: dict, project: dict):
        if not project:
            return data

        result = {}
        for k, v in project.items():
            if isinstance(v, dict) and k.startswith('$'):
                sub_key = k[1:]
                if sub_key in data:
                    result[sub_key] = data[sub_key]
            elif v == 1:
                if k in data:
                    result[k] = data[k]
            elif v == 0:
                continue
            elif isinstance(v, str) and v.startswith('$'):
                alias_key = v[1:]
                if alias_key in data:
                    result[k] = data[alias_key]
        return result

    def delete(self, filtro={}) -> DeleteResult:
        self._reload_config()
        count = self.get_config('count')
        deleted_count = 0
        stacks_folders = tools.ListCarpetas(self._ruta)

        for stack in stacks_folders:
            ruta_del_stack = f"{self._ruta}/{stack}"
            archivos = tools.ListArchivos(ruta_del_stack, '.json', True)

            left = 0
            right = len(archivos) - 1

            while left <= right:
                if left == right:
                    archivos_batch = [archivos[left]]
                else:
                    archivos_batch = [archivos[left], archivos[right]]

                for archivo in archivos_batch:
                    file_path = f"{ruta_del_stack}/{archivo}"
                    datos = tools.CargarArchivoJson(file_path)

                    if all(datos.get(k) == v for k, v in filtro.items()):
                        os.remove(file_path)
                        deleted_count += 1
                        count -= 1

                left += 1
                right -= 1

        self._modificar_config('count', count)
        return DeleteResult(deleted_count=deleted_count)

    def update(self, filtro={}, nuevos_datos={}) -> UpdateResult:
        self._reload_config()
        matched_count = 0
        modified_count = 0
        stacks_folders = tools.ListCarpetas(self._ruta)

        for stack in stacks_folders:
            ruta_del_stack = f"{self._ruta}/{stack}"
            archivos = tools.ListArchivos(ruta_del_stack, '.json', True)

            left = 0
            right = len(archivos) - 1

            while left <= right:
                if left == right:
                    archivos_batch = [archivos[left]]
                else:
                    archivos_batch = [archivos[left], archivos[right]]

                for archivo in archivos_batch:
                    file_path = f"{ruta_del_stack}/{archivo}"
                    datos = tools.CargarArchivoJson(file_path)

                    if all(datos.get(k) == v for k, v in filtro.items()):
                        matched_count += 1
                        datos.update(nuevos_datos)
                        tools.EscribirArchivoJson(file_path, datos)
                        modified_count += 1

                left += 1
                right -= 1

        return UpdateResult(matched_count=matched_count, modified_count=modified_count)

class Db:
    def __init__(self, cluster_name: str, name: str):
        self._cluster_name = cluster_name
        self.name = name
        os.makedirs(os.path.join(cluster_name, name), exist_ok = True)

    def __getitem__(self, key):
        return Collection(self._cluster_name, self.name, key)
    
    def get_collections_names(self):
        return tools.ListCarpetas(tools.RutaRelativa(f"/{self._cluster_name}/{self.name}"))
    
    def get_collections_list(self):
        return list(map(lambda dt: self.__getitem__(dt), self.get_collections_names()))
    
    def delete_collection(self, collection: Union[str, Collection]):
        if isinstance(collection, Collection):
            collection_name = collection.name
        else:
            collection_name = collection
        collection_path = tools.RutaRelativa(f"{self._cluster_name}/{self.name}/{collection_name}")

        if os.path.exists(collection_path):
            tools.EliminarDirectorio(collection_path)
        else:
            raise FileNotFoundError(f"Collection '{collection_name}' does not exist")

class Cluster:
    def __init__(self, name: str) -> None:
        self.name = name
        os.makedirs(name, exist_ok = True)

    def __getitem__(self, key):
        return Db(self.name, key)
    
    def get_databases_names(self):
        return tools.ListCarpetas(tools.RutaRelativa(f"/{self.name}"))
    
    def get_databases_list(self):
        return list(map(lambda db_name: self.__getitem__(db_name), self.get_databases_names()))
    
    def create_database(self, database_name: str):
        db_path = tools.RutaRelativa(f"/{self.name}/{database_name}")
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        else:
            raise FileExistsError(f"Database '{database_name}' already exists")
        return Db(self.name, database_name)

    def delete_database(self, database: Union[str, Db]):
        if isinstance(database, Db):
            database_name = database.name
        else:
            database_name = database
        
        db_path = tools.RutaRelativa(f"/{self.name}/{database_name}")
        
        if os.path.exists(db_path):
            tools.EliminarDirectorio(db_path)
        else:
            raise FileNotFoundError(f"Database '{database_name}' does not exist")