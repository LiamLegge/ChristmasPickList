from typing import Dict


def load_assignments(filename: str = "secret_santa.txt") -> Dict[str, str]:
	assignments = {}
	with open(filename, "r", encoding="utf-8") as input_file:
		for line_number, line in enumerate(input_file, start=1):
			line = line.strip()
			if not line:
				continue
			if "->" not in line:
				raise ValueError(f"Invalid assignment on line {line_number}.")
			giver, receiver = (part.strip() for part in line.split("->", 1))
			if not giver or not receiver:
				raise ValueError(f"Invalid assignment on line {line_number}.")
			assignments[giver] = receiver
	return assignments


if __name__ == "__main__":
	try:
		assignments = load_assignments()
	except FileNotFoundError:
		print("secret_santa.txt was not found. Run Picker.py first.")
		raise SystemExit(1)
	except ValueError as error:
		print(error)
		raise SystemExit(1)

	while True:
		name = input("Enter your name to look up, or 'q' to quit: ").strip()

		if name.lower() == "q":
			break

		if name not in assignments:
			print(f"'{name}' is not in the list.")
			continue

		print(f"{name} -> {assignments[name]}")
