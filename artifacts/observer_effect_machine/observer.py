
"""
Observer Effect Machine
-----------------------

A deterministic system whose variability emerges from the
relationship between code, execution, and interpretation.
"""

import hashlib
import inspect
import textwrap

def structural_fingerprint():
    src = inspect.getsource(structural_fingerprint)
    return hashlib.sha256(src.encode()).hexdigest()

def collapse(fingerprint):
    # Map fingerprint into pseudo-states
    value = int(fingerprint[:12], 16)
    modes = [
        "The system appears stable.",
        "The system appears unstable.",
        "The system appears recursive.",
        "The system appears observational.",
        "The system appears incomplete.",
    ]
    return modes[value % len(modes)]

def invariant(fingerprint):
    return sum(ord(c) for c in fingerprint) % 101

def run():
    fp = structural_fingerprint()
    interpretation = collapse(fp)
    inv = invariant(fp)

    print("Fingerprint      :", fp[:24], "...")
    print("Interpretation   :", interpretation)
    print("Invariant residue:", inv)

    print("\nNote:")
    print(textwrap.fill(
        "If this output feels contingent, the variability is not "
        "in the machine but in the cognitive model applied to it.",
        width=70
    ))

if __name__ == "__main__":
    run()
