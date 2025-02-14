from pymongo import MongoClient

# Conéctate a la base de datos de MongoDB (ajusta la URI a tus necesidades)
client = MongoClient('mongodb://10.57.55.181:27018/')
db = client['LibreChat']

# Definir la colección
conversations_collection = db['files']

# Pipeline de agregación
pipeline = [
    {
        '$lookup': {
            'from': 'users', 
            'localField': 'user', 
            'foreignField': '_id', 
            'as': 'user_info'
        }
    }, {
        '$match': {
            'user_info': {
                '$eq': []
            }
        }
    }
]

# Ejecutar el pipeline de agregación
cursor = conversations_collection.aggregate(pipeline)

# Eliminar cada conversación sin usuario asociado
for conversation in cursor:
    conversation_id = conversation['_id']
    result = conversations_collection.delete_one({'_id': conversation_id})
    if result.deleted_count > 0:
        print(f"Transaccion  con _id {conversation_id} eliminada.")
    else:
        print(f"No se pudo eliminar la transaccion con _id {conversation_id}.")

client.close()