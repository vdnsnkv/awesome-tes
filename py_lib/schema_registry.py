import json
from pathlib import Path

import jsonschema


def _event_key_from_path(path: Path):
    _, *event_name_parts, _ = path.parts
    event_name = "".join([p.capitalize() for p in event_name_parts])
    version = path.name.replace(path.suffix, "")
    return f"{event_name}.{version}"


def _event_key_from_event_name(event_name: str, version: int):
    return f"{event_name}.v{version}"


class SchemaRegistry:
    def __init__(self, schemas_root: str):
        self.schemas_root_path = Path(schemas_root)
        self.schemas = None
        self._load_schemas()

    def _load_schemas(self):
        self.schemas = {}
        for path in self.schemas_root_path.glob("**/*"):
            if path.is_dir():
                continue
            event_key = _event_key_from_path(path)
            self.schemas[event_key] = json.loads(path.read_bytes())
        return

    def get_schema(self, event_name: str, version: int):
        event_key = _event_key_from_event_name(event_name, version)
        return self.schemas[event_key]

    def validate(self, data, event_name: str, version: int):
        schema = self.get_schema(event_name, version)
        return jsonschema.validate(data, schema)
