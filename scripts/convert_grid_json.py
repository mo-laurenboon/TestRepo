import sys, re, os, json

#open the issue body
file = sys.argv[1]
with open(file, "r") as f:
  form = f.read()

#load in issue body
grid = {}
match = re.findall(r"### (.+?)\n(.+)", form)

#convert issue body to dictionary format
for key, value in match:
  clean = key.strip().lower().replace(" ", "")
  if clean in ("LatitudePoints", "LongitudePoints"):
    try: 
      grid[clean] = int(value.strip())
    except ValueError:
      print(f"Unable to convert {clean} to integer, storing value as string")
  else: grid[clean] = value.strip()

#setup file to be placed in grid database and named using contents values
os.makedirs("Grid_Database", exist_ok=True)
if grid['Type'] == "simple":
  type = 's'
elif grid['Type'] == "complex":
  type = 'c'

output = f"Grid_Database/g-{type}-{grid['lat-points']}-{grid['long-points']}.json"

#create json format from YAML
with open(output, "w") as f:
  json.dumps(grid, indent=2)
print(f"Json file created successfully, file saved as {output}")
print("JSON appears as follows:")
print(json.dumps(grid, indent-=2)
  
