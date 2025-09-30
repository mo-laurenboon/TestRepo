''' 
This script takes the contens of the Grid_Data_Form.yml file and parses information
to a json file that is added to grid-data base and checks for duplicate entries. It also
automatically opens a pull request for review with key information on the new grid format
parsed to the PR body.
'''

import sys, re, os, json

#open the issue body and load key-value pairs 
def load_grid_form():
  
  file = sys.argv[1]
  with open(file, "r") as f:
    form = f.read()

  grid = {}
  match = re.findall(r"### (.+?)\n\s*\n?(.+)", form)
  
  return grid, match

#convert issue body to dictionary format and clean values
def create_dict(grid, match):
  
  for key, value in match:
    clean = key.strip().lower().replace(" ", "")
    if clean in ("latitudepoints", "longitudepoints"):
      try: 
        grid[clean] = int(value.strip())
      except ValueError:
        print(f"Unable to convert {clean} to integer, storing value as string")
    else: 
      grid[clean] = value.strip()

    print("debug: available keys:", list(grid.keys()))
      
  return grid

#generate filename from form contents
def create_filename(grid):
  
  if grid['type'] == "simple":
    type = 's'
  elif grid['type'] == "complex":
    type = 'c'
    
  output = f"grid-database/g-{type}-{grid['latitudepoints']}-{grid['longitudepoints']}.json"
  
  if os.path.exists(output):
    print(f" WARNING: This grid type already exists, please see {output}")
    sys.exit(1)
    
  return type, output

#dump file contents to json and append filename to outputs
def dump_to_json(grid, output):
  with open(output, "w") as f:
    json.dumps(grid, indent=2)
  print(grid)
  print(f"Json file created successfully, file saved as {output}")

  #append file to outputs so the filename can be printed in PR body
  with open(os.environ["GITHUB_OUTPUT"], "a") as out:
    out.write(f"json_file={output}")

  
if __name__ == '__main__':

  grid, match = load_grid_form()
  grid = create_dict(grid, match)
  
  #check database directory exists
  os.makedirs("grid-database", exist_ok=True)

  #create and save json file 
  print("heres how json looks outside of the function:", grid)
  type, output = create_filename(grid)
  dump_to_json(grid, output)
