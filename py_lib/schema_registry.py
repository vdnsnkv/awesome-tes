import json
import logging
from pathlib import Path

import jsonschema

logger = logging.getLogger(__name__)


def _event_key_from_path(path: Path):
    *_, aggregate_name, event_type, _ = path.parts
    event_name = f"{aggregate_name.capitalize()}{event_type.capitalize()}"
    version = path.name.replace(path.suffix, "")
    return f"{event_name}.{version}"


def _event_key_from_event_name(event_name: str, version: int):
    return f"{event_name}.v{version}"


class SchemaRegistry:
    def __init__(self, schemas_root: str):
        self.schemas_root_path = Path(schemas_root).absolute()
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
        try:
            return self.schemas[event_key]
        except KeyError:
            logger.error(
                f"Schema not found for {event_key}, available schemas are: {self.schemas.keys()}"
            )
            raise

    def validate(self, data, event_name: str, version: int):
        if not isinstance(event_name, str):
            event_name = str(event_name)
        schema = self.get_schema(event_name, version)
        return jsonschema.validate(data, schema)
