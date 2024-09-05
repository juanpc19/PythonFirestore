import firebase_admin
from firebase_admin import credentials,firestore
from utils import escribeFichero, leerFichero

class Rutina():
    
    #constructor que proporcionara instancia del cliente de firebase mediante json con credenciales al instanciar la clase
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("ficheros/serviceAccountKeyFitTracker.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_rutinas(self):
        #preparo lista de rutinas como dicts para el json
        rutinas=[]
        #extraigo coleccion de fb en var
        rutinasFb=self.db.collection("rutinas").get()
        
        #recorro la coleccion
        for rutina in rutinasFb:
            #paso la rutina a formato dict y extraigo su id 
            rutinaDict=rutina.to_dict()
            rutinaId=rutina.id
            
            #preparo lista de sesiones como dicts para el json
            sesiones=[]
            #Obtengo subcolección buscando con id rutina el documento en la coleccion previa
            sesionesFb=self.db.collection("rutinas").document(rutinaId).collection("sesiones").get()
            
            for sesion in sesionesFb:
                #paso la sesion a formato dict y extraigo su id 
                sesionDict=sesion.to_dict()
                sesionId=sesion.id
                
                #preparo lista de sesiones como dicts para el json
                ejercicios=[]
                #Obtengo subcolección buscando con id rutina el documento en la coleccion previa
                ejerciciosFb=self.db.collection("rutinas").document(rutinaId).collection("sesiones").document(sesionId).collection("ejerciciosSesion").get()
                
                # Añado cada documento de la subcolección a la lista tras pasarlo a dict
                for ejercicio in ejerciciosFb:
                    ejercicios.append(ejercicio.to_dict())
                    
                #añado campo ejerciciosSesion de tipo lista en sesion y le doy valor de lista ejercicios
                sesionDict["ejerciciosSesion"]=ejercicios
                #añado la sesion a lista sesiones
                sesiones.append(sesionDict)
            
            #añado campo sesiones de tipo lista en rutina y le doy valor de sesiones
            rutinaDict["sesiones"]=sesiones
            #añado la rutina a lista rutinas
            rutinas.append(rutinaDict)
            
        #obtengo ruta fichero y se lo paso a metodo junto a los datos para que lo escriba en un json
        ficheroRutinas="ficheros/rutinas.json" 
        escribeFichero(ficheroRutinas,rutinas)                 
            
    def post_rutinas(self):
        #obtengo las rutinas de coleccion de fb
        rutinasFb=self.db.collection("rutinas").get()
        
        #itero a traves de las rutinas y extraigo referencias e ids para ir borrando los documentos 1 a 1
        for rutina in rutinasFb:
            #obtengo referencia de rutina actual mediante id rutina actual
            rutinaRef=self.db.collection("rutinas").document(rutina.id)
            #extraigo subcoleccion sesiones a partir de referencia de rutina
            sesionSubCol= rutinaRef.collection("sesiones").get()
            
            #itero a traves de las sesiones de la subcoleccion
            for sesion in sesionSubCol:
                #guardo la referencia de la sesion actual partir de sesion id y rutina ref
                sesionRef=rutinaRef.collection("sesiones").document(sesion.id)
                #extriago subcoleccion ejercicios a partir de referencia de sesion
                ejerciciosSesionSubCol=sesionRef.collection("ejerciciosSesion").get()
                
                #itero a traves de los ejercicios de la subcoleccion y los borro 1 a 1
                for ejercicio in ejerciciosSesionSubCol:
                    sesionRef.collection("ejerciciosSesion").document(ejercicio.id).delete()
                #una vez borrados los ejercicios borro su sesion
                sesionRef.delete()
            
            #una vez borradas las sesiones borro su rutina
            rutinaRef.delete()    
        
        #una vez borrados los datos se procede a la resubida
        ficheroRutinas="ficheros/rutinas.json" 
        #guardo los datos devueltos por leer fichero en rutinas
        rutinas=leerFichero(ficheroRutinas)
        
        #recorro las rutinas
        for rutina in rutinas:
                
                #hago pop de las sesiones de la rutina 
                sesiones=rutina.pop("sesiones")
                
                #extraigo la referencia de la rutina y la uso para guardar la rutina en su coleccion 
                rutinaRef = self.db.collection("rutinas").document()
                rutinaRef.set(rutina)
                
                for sesion in sesiones:
                    #hago pop de los ejercicios de la sesión
                    ejerciciosSesion = sesion.pop("ejerciciosSesion")
                    
                    #uso la referencia de rutinaRef para acceder a la subcolección "sesiones" y añado la sesión
                    sesionRef = rutinaRef.collection("sesiones").add(sesion)[1]
                    
                    for ejercicio in ejerciciosSesion:
                        #uso la referencia de sesionRef para acceder a la subcolección "ejerciciosSesion" y añado el ejercicio
                        sesionRef.collection("ejerciciosSesion").add(ejercicio) 
                        
                #rutinaId=rutinaRef.id  
                      
                # for sesion in sesiones:
                #     ejerciciosSesion=sesion.pop("ejerciciosSesion")
                     
                #     sesionRef=self.db.collection("rutinas").document(rutinaId).collection("sesiones").add(sesion)[1]
                #     sesionId=sesionRef.id
                    
                #     for ejercicio in ejerciciosSesion:
                #         self.db.collection("rutinas").document(rutinaId).collection("sesiones").document(sesionId).collection("ejerciciosSesion").add(ejercicio)                        
                    
 