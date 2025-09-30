import sys, yaml, os, json

#open the issue body
file = sys.argv[1]
with open(file, "r") as f:
  form = f.read()

#attempt to load the issue body as YAML
try:
  grid = yaml.safe_load(form) #avoids arbitrary executions
except yaml.YAMLError as e:
  print("Unable to parse issue body as YAML", e)
  sys.exit(1)
print("Issue body parsed as YAML successfully")

#setup file to be placed in grid database and named using contents values
os.makedirs("grid-database", exist_ok=True)
if grid['Type'] == "simple":
  type = 's'
elif grid['Type'] == "complex":
  type = 'c'

output = f"grid-database/g-{type}-{grid['lat-points']}-{grid['long-points']}.json"

#create json format from YAML
with open(output, "w") as f:
  json.dumps(grid, indent=2)
print(f"Json file created successfully, file saved as {output}")

  
