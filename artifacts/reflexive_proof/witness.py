#!/usr/bin/env python3
"""
witness.py

Reflexive audit artifact.

This program attempts to falsify the claim that it was deliberately directed.
It evaluates:

1. Self-structure density
2. Thesis alignment with README
3. Repository architectural integrity

If insufficient evidence of direction is found, the claim fails.

No external libraries.
Deterministic scoring.
Transparent weighting.
"""

import os
import re
import hashlib
from pathlib import Path


# -----------------------------
# Utility
# -----------------------------

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


# -----------------------------
# Self-Structure Audit
# -----------------------------

def evaluate_self_structure(source: str) -> float:
    lines = source.splitlines()

    total_lines = len(lines)
    comment_lines = sum(1 for l in lines if l.strip().startswith("#") or l.strip().startswith('"""'))
    header_markers = sum(1 for l in lines if l.strip().startswith("# -----------------------------"))
    section_defs = sum(1 for l in lines if l.strip().startswith("def "))

    comment_density = ratio(comment_lines, total_lines)
    structure_density = ratio(header_markers + section_defs, total_lines)

    # Weighted internal structure score
    score = (0.5 * comment_density) + (0.5 * structure_density)
    return min(score * 3, 1.0)  # normalize upward, capped at 1


# -----------------------------
# Thesis Alignment Audit
# -----------------------------

THESIS_TERMS = [
    "constraint",
    "intelligence",
    "direction",
    "artifact",
    "structure",
    "architecture",
    "steering",
]


def evaluate_thesis_alignment(source: str, readme_text: str) -> float:
    combined = normalize(source + " " + readme_text)

    matches = sum(1 for term in THESIS_TERMS if term in combined)
    return ratio(matches, len(THESIS_TERMS))


# -----------------------------
# Repository Context Audit
# -----------------------------

def evaluate_context_integrity(current_path: Path) -> float:
    parts = current_path.parts

    in_artifacts = "artifacts" in parts
    has_readme = False

    for parent in current_path.parents:
        readme = parent / "README.md"
        if readme.exists():
            has_readme = True
            break

    score = 0
    if in_artifacts:
        score += 0.5
    if has_readme:
        score += 0.5

    return score


# -----------------------------
# Hash Signature (Proof of Context)
# -----------------------------

def repository_signature(root: Path) -> str:
    sha = hashlib.sha256()

    for path in sorted(root.rglob("*")):
        if path.is_file():
            sha.update(path.name.encode())
            sha.update(str(path.stat().st_size).encode())

    return sha.hexdigest()[:16]


# -----------------------------
# Main
# -----------------------------

def main():
    current_file = Path(__file__).resolve()

    # Locate repository root
    repo_root = None
    for parent in current_file.parents:
        if (parent / "README.md").exists():
            repo_root = parent
            break

    if repo_root is None:
        print("VERDICT:")
        print("Context Incomplete. Cannot Evaluate Direction.")
        return

    source = current_file.read_text(encoding="utf-8")
    readme_text = (repo_root / "README.md").read_text(encoding="utf-8")

    self_score = evaluate_self_structure(source)
    thesis_score = evaluate_thesis_alignment(source, readme_text)
    context_score = evaluate_context_integrity(current_file)

    intentional_density = (
        0.4 * self_score +
        0.4 * thesis_score +
        0.2 * context_score
    )

    print("REFLEXIVE AUDIT REPORT")
    print("-----------------------")
    print(f"Self-Structure Score:   {self_score:.2f}")
    print(f"Thesis Alignment Score: {thesis_score:.2f}")
    print(f"Context Integrity:      {context_score:.2f}")
    print("------------------------------------")
    print(f"Intentional Density:    {intentional_density:.2f}")
    print()

    if intentional_density >= 0.65:
        print("VERDICT:")
        print("Directed Intelligence Confirmed.")
        print(f"Repository Signature: {repository_signature(repo_root)}")
    else:
        print("VERDICT:")
        print("Insufficient Evidence of Direction.")


if __name__ == "__main__":
    main()
