import sys, json
d = json.load(sys.stdin)
p = d["data"]["content"][0]
print("has imageData:", "imageData" in p)
print("imageUrl:", p.get("imageUrl", ""))
if "imageData" in p:
    print("imageData length:", len(p["imageData"]))
    print("imageData starts with:", p["imageData"][:30])
