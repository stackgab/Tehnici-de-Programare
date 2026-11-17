import hashlib
import re
import base64
import argparse, json
from urllib.parse import unquote
# A1
s = "Salut"
b = s.encode()  # bytes
print(b, b[0])  # b"Salut" 83

print(b.hex())
b2 = bytes.fromhex(b.hex())
print(b2)


# A2
def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"

    return "necunoscut"
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
# A3
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode()
    else:
        return "necunoscut", b""

    return strat, rezultat

# A4
def citibil(b):
    return all(32 <= c < 127 for c in b)


val = "NTM1OTU3NTk="

for _ in range(8):
    strat, b = desfa(val)

    if citibil(b):
        print(b.decode())
        break

    val = b.decode()

#A5
date = open("probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar):
        print("cheie:", k, clar.decode())
#A6
tinta = open("probe/hashuri.txt").readline().strip()
print(len(tinta))

for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()

    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break

#A7
#A7
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
        intrare = date.decode("utf-8")
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode("utf-8", errors="replace")
    }

    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)
