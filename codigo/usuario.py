import firebase_admin
from firebase_admin import credentials,firestore
from utils import escribeFichero, leerFichero

class Usuario():
    
    #constructor que proporcionara instancia del cliente de firebase mediante json con credenciales al instanciar la clase
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("ficheros/serviceAccountKeyFitTracker.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()        

    def get_usuarios(self):
        #preparo lista de dicts para el json
        usuarios=[]
        #extraigo coleccion de fb en var
        usuariosFb=self.db.collection("usuarios").get()

        #recorro la coleccion 
        for usuario in usuariosFb:
            
            #paso el usuario a formato dict y extraigo su id
            usuarioDict = usuario.to_dict()
            usuarioId = usuario.id
            # Obtengo subcolección buscando con id usuario el documento en la coleccion previa
            subcoleccionFb = self.db.collection("usuarios").document(usuarioId).collection("ejerciciosPersonalizados").get()
            #preparo lista de ejercicios como dicts para el json
            ejerciciosPersonalizados = []
            
            for doc in subcoleccionFb:
                # Añado cada documento de la subcolección a la lista tras pasarlo a dict
                ejerciciosPersonalizados.append(doc.to_dict())        
            #añado campo ejerciciosPersonalizados de tipo lista en usuario
            usuarioDict["ejerciciosPersonalizados"] = ejerciciosPersonalizados
            
            #una vez añadidos los ejercicios al usuario añado este a la lista de usuarios
            usuarios.append(usuarioDict)
        
        #obtengo ruta fichero y se lo paso a metodo junto a los datos para que lo escriba en un json
        ficheroUsuarios="ficheros/usuarios.json" 
        escribeFichero(ficheroUsuarios,usuarios)
        
    def post_usuarios(self):
        #obtengo los usuarios de la coleccion de fb
        usuariosFb=self.db.collection("usuarios").get()
        
        #extraigo id de documentos de coleccion y lo uso para borrarlos 1 a 1
        for usuario in usuariosFb:
            id=usuario.id #obtengo id de usuario actual
            #guardo la referencia del usuario actual a partir del id
            usuarioRef = self.db.collection("usuarios").document(id)
            # la uso para obtener referencia a la subcolección de 'ejerciciosPersonalizados' para el usuario actual
            ejerciciosSubcol = usuarioRef.collection("ejerciciosPersonalizados").get()
            
            # borro todos los documentos en la subcolección 'ejerciciosPersonalizados'
            for ejercicio in ejerciciosSubcol:
                usuarioRef.collection("ejerciciosPersonalizados").document(ejercicio.id).delete()
            
            # borro el documento del usuario
            usuarioRef.delete()
            
        #una vez borrados se procede a la escritura
        ficheroUsuarios="ficheros/usuarios.json"   
        #preparo lista de dicts para el json
        usuarios=[]
        #extraigo datos del json con funcion
        usuarios=leerFichero(ficheroUsuarios)
        
        #creo id a partir del escrito en el json en campo id
        for usuario in usuarios:
            #extraido el id del usuario para usarlo en creacion del mismo en la bbdd y para indicar donde crear la subcoleccion
            id=usuario.get("userId")
            idCadena=str(id)
            
            #extraigo los ejercicios del usuario con pop
            ejerciciosDeUsuario=usuario.pop("ejerciciosPersonalizados")
           
            #inserto el usuario   
            self.db.collection("usuarios").document(idCadena).set(usuario)
            
            #inserto ejercicios en subcoleccion de usuario
            for ejercicio in ejerciciosDeUsuario:
                self.db.collection("usuarios").document(idCadena).collection("ejerciciosPersonalizados").add(ejercicio)
            