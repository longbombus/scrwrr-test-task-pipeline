import json
import sys

import assets
import validation

def read_json_from_stdin() -> dict:
	raw = sys.stdin.read()
	try:
		return json.loads(raw)
	except json.JSONDecodeError as exc:
		raise SystemExit(f"Invalid JSON on stdin: {exc}") from exc


def read_json_from_file(path: str) -> dict:
	try:
		with open(path, "r", encoding="utf-8") as handle:
			return json.load(handle)
	except FileNotFoundError as exc:
		raise SystemExit(f"File not found: {path}") from exc
	except json.JSONDecodeError as exc:
		raise SystemExit(f"Invalid JSON in file {path}: {exc}") from exc

def main() -> None:
	if len(sys.argv) > 1:
		data = read_json_from_file(sys.argv[1])
	else:
		data = read_json_from_stdin()
	assets_list = assets.parse_assets(data)

	alerts = validation.validate(assets_list)

	for severity, items in alerts.items():
		print(f"{severity}s:")
		for asset_info, alert in items:
			print(f"Asset `{asset_info.name}`: {alert.description}")

	if "Error" in alerts:
		print("FAIL")
	else:
		print("PASS")

if __name__ == "__main__":
	main()
