""" 
This script takes the contens of the Grid_Data_Form.yml file and parses information to a json file
that is added to grid-data base and checks for duplicate entries. It also automatically opens a
pull request for review with key information on the new grid formatparsed to the PR body.
"""

import argparse
import re
import os
import sys 
import json


#open the issue body and load key-value pairs 
def load_grid_form():
  """
  Loads the issue body from the form and identifies key-value pairs.

  :returns: grid form contents 
  """
  parser = argparse.ArgumentParser(description="Open issue body")
  parser.add_argument("file", help="The issue body to process")
  args = parser.parse_args()

  with open(args.file, "r") as f:
    form = f.read()

  match = re.findall(r"### (.+?)\n\s*\n?(.+)", form)
  
  return match


#convert issue body to dictionary format and clean values
def create_dict(match):
  """
  Generates a dictionary format from the loaded form contents and cleans the key-value pairs to 
  ensure consistent formatting.

  :param grid: the name of the dictionary 
  :param match: the identified key value pairs from the form
  :returns: dictionary containing the grid parameters from the form
  :raises ValueError: raises an exception if the number of lat or long points connot be converted 
                      to an integer value
  """
  grid = {}

  for key, value in match:
    clean = key.strip().lower().replace(" ", "")
    if clean in ("latitudepoints", "longitudepoints"):
      try: 
        grid[clean] = int(value.strip())
      except ValueError:
        print(f"Unable to convert {clean} to integer, storing value as string")
    else: 
      grid[clean] = value.strip()
      
  return grid


#generate filename from form contents
def create_filename(grid):
  """
  Generates consistantly formatted filename from the form contents e.g.
  'g-<type>-<number of latitude points>-<number of longitude points>.json'.

  :param grid: dictionary containing the grid parameters from the form
  :returns: formatted filename of the json file
  """
  if grid['type'] == "simple":
    type = 's'
  elif grid['type'] == "complex":
    type = 'c'
    
  output = f"grid-database/g-{type}-{grid['latitudepoints']}-{grid['longitudepoints']}.json"
  
  if os.path.exists(output):
    print(f" WARNING: This grid type already exists, please see {output}")
    sys.exit(1)
    
  return output


#dump file contents to json and append filename to outputs
def dump_to_json(grid, output):
  """
  Dumps and writes the dictionary contents to a json file with the formatted name. The function 
  also outputs the filename as a variable so it cant be printed to the body of the PR.

  :param grid: dictionary containing the grid parameters from the form
  :param output: formatted filename of the json file
  """
  with open(output, "w") as f:
    f.write(json.dumps(grid, indent=2))
  print(f"Json file created successfully, file saved as {output}")
  #append filename to outputs to be printed in PR body
  with open(os.environ["GITHUB_OUTPUT"], "a") as out:
    out.write(f"json_file={output}")

  
if __name__ == '__main__':

  match = load_grid_form()
  grid = create_dict(match)
  
  #check database directory exists
  os.makedirs("grid-database", exist_ok=True)

  #create and save json file 
  output = create_filename(grid)
  dump_to_json(grid, output)
