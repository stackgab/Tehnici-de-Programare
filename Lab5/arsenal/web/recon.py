#A1, A6
import requests, json, re, argparse

p = argparse.ArgumentParser()

p.add_argument("tinta")
p.add_argument("--wordlist", default=None)

a = p.parse_args()

tinta = a.tinta

r_principal = requests.get(tinta) # Get method HTTP la url variabilei tinta

print("Cod HTTP:", r_principal.status_code) # Output cu codul HTTP (200 daca totul e ok)

print("Server:", r_principal.headers.get("Server")) # Versiunea serverului
print("X-Powered-By:", r_principal.headers.get("X-Powered-By"))

#A2
r = requests.get(tinta + "/robots.txt") # Cererea robots.txt

if r.status_code == 200: # Daca HTTP e 200 (OK)
    print("robots.txt gasit:")
    print(r.text)

    for linie in r.text.splitlines(): # Dintr-un string fac o lista de linii
        if "Disallow:" in linie: # Daca se gaseste "Disallow:", se afiseaza
            print(linie)
else:
    print("robots.txt nu exista") # In caz de alt cod HTTP

#A3
if a.wordlist:
    with open(a.wordlist) as f:
        cuvinte = [linie.strip() for linie in f]
else:
    cuvinte = [
        "admin",
        "login",
        "backup",
        "config",
        "test",
        "uploads",
        "phpmyadmin"
    ] # Parcurgerea folosind aceasta lista

gasite = []

for c in cuvinte: # Iteratie pentru fiecare element din lista
    r = requests.get(tinta + "/" + c) # Se cauta calea

    if r.status_code == 200: # Daca raspunde cu 200 OK
        gasite.append(c)

    elif r.status_code == 403: # Forbidden
        print("interzis (interesant):", c)

print("gasite:", gasite)

#A4
r = requests.get(tinta + "/")

linkuri = re.findall(r'href="([^"]+)"', r.text) # Extragerea valorilor href

print(set(linkuri)) # Eliminarea duplicatelor

#A7
fisa = {
    "tinta": tinta,
    "server": r_principal.headers.get("Server"),
    "directoare": gasite
}

with open("arsenal/web/fisa.json", "w") as f:
    json.dump(fisa, f, indent=2)

print("fisa salvata:", fisa)