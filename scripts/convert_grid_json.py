import sys, re, os, json

#open the issue body
file = sys.argv[1]
with open(file, "r") as f:
  form = f.read()

#load in issue body and ey value pairs
grid = {}
match = re.findall(r"### (.+?)\n\s*\n?(.+)", form)
#convert issue body to dictionary format
for key, value in match:
  clean = key.strip().lower().replace(" ", "")
  if clean in ("latitudepoints", "longitudepoints"):
    try: 
      grid[clean] = int(value.strip())
    except ValueError:
      print(f"Unable to convert {clean} to integer, storing value as string")
  else: grid[clean] = value.strip()

#setup file to be placed in grid database and named using contents values
os.makedirs("Grid_Database", exist_ok=True)
if grid['type'] == "simple":
  type = 's'
elif grid['type'] == "complex":
  type = 'c'
output = f"Grid_Database/g-{type}-{grid['latitudepoints']}-{grid['longitudepoints']}.json"
if os.path.exists(output):
  print(f" WARNING: This grid type already exists, please see {output}")
  sys.exit(1)
  
#dump to json file
with open(output, "w") as f:
  json.dumps(grid, indent=2)
print(f"Json file created successfully, file saved as {output}")
