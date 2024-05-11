# Input de texto
nombre = input("Ingresa tu nombre: ")
print("Hola,", nombre)

# Input de número entero
edad = int(input("\nIngresa tu edad: "))
if edad >= 18:
    print("Eres mayor de edad.\n")
else:
    print("Eres menor de edad.\n")

# Lista de números
numeros = [1, 2, 3, 4, 5]

# Bucle for para recorrer la lista
for numero in numeros:
    if numero % 2 == 0:
        print(numero, "es par.")
    else:
        print(numero, "es impar.")

# Input de opción
opcion = input("\n¿Te gusta Python? (s/n): ")
if opcion.lower() == 's':
    print("¡Excelente!")
elif opcion.lower() == 'n':
    print("Qué lástima.")
else:
    print("Respuesta no válida.")
