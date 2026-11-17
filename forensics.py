
import re
from PIL import Image
from PIL.ExifTags import TAGS

# B1 - Identificarea tipului real al fisierului
def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()


print(tip_real("probe/foto.jpg"))


# B2 - Extragerea sirurilor ASCII
date = open("probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())


# B3 - Extragerea metadatelor EXIF
exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

# GPS
gps = exif.get(34853)
print("GPS:", gps)

if gps:
    lat = gps[2]
    lon = gps[4]

    lat_zecimal = lat[0] + lat[1] / 60 + lat[2] / 3600
    lon_zecimal = lon[0] + lon[1] / 60 + lon[2] / 3600

    if gps[1] == "S":
        lat_zecimal = -lat_zecimal

    if gps[3] == "W":
        lon_zecimal = -lon_zecimal

    print("Latitudine:", float(lat_zecimal))
    print("Longitudine:", float(lon_zecimal))


# B4 - Carving: extragerea arhivei ZIP
date = open("probe/ascuns.png", "rb").read()

i = date.find(b"PK\x03\x04")

if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:])

    print("arhiva extrasa de la octetul", i)


# B5 - Ascunderea mesajului prin LSB
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)
biti += "00000000"  # Octetul 0 marcheaza sfarsitul mesajului

px_nou = []
i = 0

for r, g, b in px:
    canale = [r, g, b]

    for j in range(3):
        if i < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[i])
            i += 1

    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")

print("Mesaj ascuns in stego.png")


# B6 - Extragerea mesajului prin LSB
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""

for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

# Grupeaza cate 8 biti -> octeti -> text
mesaj = b""

for i in range(0, len(biti) - 7, 8):
    octet = int(biti[i:i+8], 2)

    if octet == 0:
        break

    mesaj += bytes([octet])

print("Mesaj dezvaluit:", mesaj.decode("utf-8"))
