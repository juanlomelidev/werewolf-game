import random

# crear arreglos para los roles especiales, de lobo y de villagers
# witch:
# sorcerer:
# seer:
# hunter:
# mayor:

special_roles = ["witch", "sorcerer", "seer", "hunter", "mayor"]
villager_roles = ["villager"]
wolf_roles = ["wolf"]

# ver cuantos jugadores habra en la partida
players = int(input("Escoge el número de jugadores (8-16): "))

# cambia la cantidad de lobos dependiendo de la cantidad de jugadores
if 8 <= players <= 10:
    wolf_roles = ["wolf"]
elif 11 <= players <= 13:
    wolf_roles = ["wolf", "wolf"]
elif 14 <= players <= 16:
    wolf_roles = ["wolf", "wolf", "wolf"]
else:
    print("Número de jugadores fuera del rango permitido (8-16).")
    exit()

# crear la lista definitiva que mete los roles especiales y los lobos, y al final lo sobrante son los villagers
roles = special_roles + wolf_roles
roles_villager_count = players - len(roles)
roles += villager_roles * roles_villager_count

# mezclar aleatoreamente la lista
random.shuffle(roles)

# imprimir la lista
for i in range(players):
    print(f"Player {i + 1}: {roles[i]}")

