import firebase_admin
from firebase_admin import credentials,firestore
from utils import escribeFichero, leerFichero

class Consejo():
    
    #constructor que proporcionara instancia del cliente de firebase mediante json con credenciales al instanciar la clase
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("ficheros/serviceAccountKeyFitTracker.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
    def get_consejos(self):
        #preparo lista de dicts para el json
        consejos=[]
        #extraigo coleccion de fb en var
        consejosFb=self.db.collection("consejos").get() 

        #recorro la coleccion 
        for consejo in consejosFb:
            #añado a lista
            consejos.append(consejo.to_dict())
        #ordeno por id antes de escribir en fichero    
        consejos.sort(key=lambda x: x["id"])
        
        #obtengo ruta fichero y se lo paso a metodo junto a los datos para que lo escriba en un json 
        ficheroPersonas="ficheros/consejos.json" 
        escribeFichero(ficheroPersonas,consejos)
        
    def post_consejos(self):
        #obtengo los consejos de la coleccion de fb
        consejosFb=self.db.collection("consejos").get()
        #extraigo id de documentos de coleccion y lo uso para borrarlos 1 a 1
        for consejo in consejosFb:
            id=consejo.id
            self.db.collection("consejos").document(id).delete()
            
        #una vez borrados se procede a la escritura
        ficheroConsejos="ficheros/consejos.json"   
        #preparo lista de dicts para el json
        consejos=[]
        #extraigo datos del json con funcion
        consejos=leerFichero(ficheroConsejos)
        #creo id a partir del escrito en el json en campo id
        for consejo in consejos:
            id=consejo.get("id")
            idCadena=str(id)
            #se crea el documento con el id creado extrayendo la info y el id del json
            self.db.collection("consejos").document(idCadena).set(consejo)
            
