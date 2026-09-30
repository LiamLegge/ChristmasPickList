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

def write_assignments_to_file(assignments: Dict[str, str], filename: str = "secret_santa.txt") -> None:
    with open(filename, "w", encoding="utf-8") as output_file:
        for giver, receiver in assignments.items():
            output_file.write(f"{giver} -> {receiver}\n")

if __name__ == "__main__":
    participants = {
        "Liam": ["Madison", "Aaron", "Lisa", "BJ"],
        "Madison": ["Aaron", "Liam", "Lisa", "BJ"],
        "Aaron": ["Liam", "Madison", "Lisa", "BJ"],
        "Lisa": ["Liam", "Madison", "Aaron", "BJ"],
        "BJ": ["Liam", "Madison", "Aaron", "Lisa"],
        "Steve": ["Moira"],
        "Moira": ["Steve"],
        "Amanda": ["Jeff", "Amber", "Josh", "Chase"],
        "Jeff": ["Amanda", "Amber", "Josh", "Chase"],
        "Amber": ["Josh", "Amanda", "Jeff", "Chase"],
        "Josh": ["Amber", "Amanda", "Jeff", "Chase"],
        "Chase": ["Amanda", "Jeff", "Amber", "Josh"],
        "Mona": ["Ralph"],
        "Ralph": ["Mona"],
    }

    seed = None
    result = pick_secret_santa_numbers(participants, seed)
    if result is None:
        print("No valid assignment found.")
    else:
        output_filename = "secret_santa.txt"
        write_assignments_to_file(result, output_filename)
        print(f"Assignments written to {output_filename}.")