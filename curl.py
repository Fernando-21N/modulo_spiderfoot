import os
import subprocess

# Construí este archivo para realizar el proceso y obtener el contenido que quería que me arroje, luego de esto
# pegue el proceso en su correspondiente archivo "sfp_cookies.py", ajustandolo de acuerdo a sus variables, etc.

os.system('clear')

print("Introduce Nombre de Dominio: ", end= ' ')  # ejemplo: https://www.example.com/
domain =  input()

# En esta siguiente línea comentada está otra opción para la recogida de cookies de un dominio web utilizando
# el comando curl, junto al parámetro --cookie-jar y registrandolas en un archivo "cjar", además de también poder
# resgistar el contenido en un index.html

# result = subprocess.run(["curl","--cookie-jar","cjar","--output","index.html", domain], stdout=subprocess.PIPE)

result = subprocess.run(["curl","-I", "--output","info", domain], stdout=subprocess.PIPE)

cookies = result.stdout.decode('utf-8')

with open("info", "r") as f:
    datafile = f.readlines()
    for linea in datafile:
        if 'set-cookie' in linea:
            cookie = linea
    

evt = ("TARGET_WEB_COOKIE", cookie)
print(evt)    