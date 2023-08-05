from pathlib import Path

import yaml


def read_yaml(file_path):
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("YAML file not found")
    except yaml.YAMLError as exc:
        print("Invalid YAML file")
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))


def get_offset():
    base_path = Path(__file__).parent
    file_path = base_path / "../../config/offset.yaml"
    data = read_yaml(file_path)
    return data["OFFSET"]


def update_offset(new_offset):
    file_path = "../../../config/offset.yaml"
    data = read_yaml(file_path)
    data["OFFSET"] = new_offset
    with open(file_path, "w") as f:
        yaml.safe_dump(data, f)
