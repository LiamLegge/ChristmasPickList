import random
from typing import Dict, List, Optional, Set

def pick_secret_santa_numbers(participants: Dict[str, List[str]], seed: Optional[int] = None) -> Optional[Dict[str, str]]:
    rng = random.Random(seed)
    names = list(participants.keys())
    n = len(names)
    idx = {name: i for i, name in enumerate(names)}
    # build allowed sets using indices
    allowed = {i: set(range(n)) - {i} - {idx[b] for b in participants.get(names[i], []) if b in idx} for i in range(n)}
    if any(len(opts) == 0 for opts in allowed.values()):
        return None

    def backtrack(assign: Dict[int, int], remaining: Set[int]) -> Optional[Dict[int, int]]:
        if len(assign) == n:
            return dict(assign)
        unassigned = [i for i in range(n) if i not in assign]
        unassigned.sort(key=lambda g: len(allowed[g] & remaining))
        giver = unassigned[0]
        choices = list(allowed[giver] & remaining)
        rng.shuffle(choices)
        for receiver in choices:
            assign[giver] = receiver
            res = backtrack(assign, remaining - {receiver})
            if res:
                return res
            del assign[giver]
        return None

    numeric_result = backtrack({}, set(range(n)))
    if numeric_result is None:
        return None
    return {names[g]: names[r] for g, r in numeric_result.items()}

if __name__ == "__main__":
    participants = {
        "Liam": ["Madison", "Lisa"],
        "Madison": ["Liam", "Lisa"],
        "Lisa": ["Liam", "Madison"],
        "Steven": ["Moira"],
        "Moira": ["Steven"],
        "Amanda": ["Amber"],
        "Amber": ["Amanda"],
    }

    seed = 42
    result = pick_secret_santa_numbers(participants, seed)
    if result is None:
        print("No valid assignment found.")
    else:
        while True:
            name = input("Enter a name to look up, 'all' to print the list, or 'q' to quit: ").strip()

            if name.lower() == "q":
                break

            if name.lower() == "all":
                for giver, receiver in result.items():
                    print(f"{giver} -> {receiver}")
                continue

            if name not in result:
                print(f"'{name}' is not in the list.")
                continue

            line = f"{name} -> {result[name]}"
            print(line)
            input("Press Enter to clear the line...")  # wait for user to read it
            print("\r" + " " * (len(line) + 10) + "\r", end="")