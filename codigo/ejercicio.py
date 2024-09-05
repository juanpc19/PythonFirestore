import firebase_admin
from firebase_admin import credentials,firestore
from utils import escribeFichero, leerFichero

class Ejercicio():
    
    #constructor que proporcionara instancia del cliente de firebase mediante json con credenciales al instanciar la clase    
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("ficheros/serviceAccountKeyFitTracker.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_ejercicios(self):
        #preparo lista de dicts para el json
        ejercicios=[]
        #extraigo coleccion de fb en var
        ejerciciosFb=self.db.collection("ejercicios").get()

        #recorro la coleccion 
        for ejercicio in ejerciciosFb:
            #añado a lista
            ejercicios.append(ejercicio.to_dict())    
        #ordeno por id antes de escribir en fichero    
        ejercicios.sort(key=lambda x: x["id"])
        
        #obtengo ruta fichero y se lo paso a metodo junto a los datos para que lo escriba en un json
        ficheroPersonas="ficheros/ejercicios.json" 
        escribeFichero(ficheroPersonas,ejercicios)
    
    def post_ejercicios(self):
        #obtengo los ejercicios de la coleccion de fb
        ejerciciosFb=self.db.collection("ejercicios").get()
        #extraigo id de documentos de coleccion y lo uso para borrarlos 1 a 1
        for ejercicio in ejerciciosFb:
            id=ejercicio.id
            self.db.collection("ejercicios").document(id).delete()
            
        #una vez borrados se procede a la escritura
        ficheroeEjercicios="ficheros/ejercicios.json"   
        #preparo lista de dicts para el json
        ejercicios=[]
        #extraigo datos del json con funcion
        ejercicios=leerFichero(ficheroeEjercicios)
        #creo id a partir del escrito en el json en campo id
        for ejercicio in ejercicios:
            id=ejercicio.get("id")
            idCadena=str(id)
            #se crea el documento con el id creado extrayendo la info y el id del json
            self.db.collection("ejercicios").document(idCadena).set(ejercicio)
            
