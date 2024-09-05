from rutina import Rutina
from usuario import Usuario
from ejercicio import Ejercicio
from consejo import Consejo

def mostrar_menu():
    print("Seleccione su opción: ")
    print()
    print("1. Bajar datos consejos")
    print("2. Bajar datos ejercicios")
    print("3. Bajar datos usuarios")
    print("4. Bajar datos rutinas")
    print()
    print("5. Resubir datos consejos")
    print("6. Resubir datos ejercicios")
    print("7. Resubir datos usuarios")
    print("8. Resubir datos rutinas")
    print()
    print("0. Cerrar consola")
    print()
    
def menu():
    consejo=Consejo()
    ejercicio=Ejercicio()
    usuario=Usuario()
    rutina=Rutina()
    
    while True:
        mostrar_menu()
        opcion = input()

        if opcion == '1':
            consejo.get_consejos()
        elif opcion == '2':
            ejercicio.get_ejercicios()
        elif opcion == '3':
            usuario.get_usuarios()
        elif opcion == '4':
            rutina.get_rutinas()
        elif opcion == '5':
            consejo.post_consejos()
        elif opcion == '6':
            ejercicio.post_ejercicios()
        elif opcion == '7':
            usuario.post_usuarios()
        elif opcion == '8':
            rutina.post_rutinas()
        elif opcion == '0':
            print("Cerrando...")
            break
        else:
            print("Opcion no válida, por favor intentelo de nuevo.")
            
if __name__ == "__main__":
    menu()
    