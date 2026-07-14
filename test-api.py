import sys, json
d = json.load(sys.stdin)
p = d["data"]["content"][0]
print("Product:", p["name"])
print("imageData:", len(p.get("imageData", "")), "bytes")
print("Has image:", "OK" if len(p.get("imageData", "")) > 5000 else "SMALL")
