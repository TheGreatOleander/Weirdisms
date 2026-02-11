"""
Temporal Interference Engine
----------------------------

A tiny machine that refuses to fully commit to a single past.

Run multiple times. Compare outputs. Notice that nothing
actually changed except your interpretation of sequence.
"""

def interfere(state):
    # Deterministic transformation
    return (state * 3 + 1) % 97

def reframe(history):
    # Rewrite history without altering facts
    return list(reversed(history))

def run(seed=1, steps=12):
    state = seed
    history = []

    for _ in range(steps):
        state = interfere(state)
        history.append(state)

    observed = reframe(history)

    print("Canonical timeline :", history)
    print("Observed timeline  :", observed)
    print("Invariant checksum :", sum(history) % 97)

if __name__ == "__main__":
    run()
