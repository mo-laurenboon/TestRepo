import yaml

if __name__ == '__main__':
    file = open("example-form-output.yml", r)
    dict = yaml.safe_load(file)