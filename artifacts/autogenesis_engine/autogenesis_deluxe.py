
import os
import hashlib
import math
from pathlib import Path
from datetime import datetime

def compute_repo_data(root: Path):
    sha = hashlib.sha256()
    file_count = 0
    total_bytes = 0
    depths = []
    entropy_accumulator = []

    for path in sorted(root.rglob("*")):
        if path.is_file():
            file_count += 1
            rel = path.relative_to(root)
            depths.append(len(rel.parts))
            data = path.read_bytes()
            total_bytes += len(data)

            sha.update(str(rel).encode())
            sha.update(data)
            entropy_accumulator.extend(data)

    fingerprint = sha.hexdigest()
    max_depth = max(depths) if depths else 0
    entropy = calculate_entropy(entropy_accumulator)

    return fingerprint, file_count, total_bytes, max_depth, entropy

def calculate_entropy(byte_data):
    if not byte_data:
        return 0.0
    freq = {}
    for b in byte_data:
        freq[b] = freq.get(b, 0) + 1
    total = len(byte_data)
    entropy = -sum((count/total) * math.log2(count/total) for count in freq.values())
    return round(entropy, 5)

def generate_outputs(root, data):
    fingerprint, file_count, total_bytes, max_depth, entropy = data

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Weirdisms Identity Report</title>
<style>
body {{ background:#111; color:#0f0; font-family: monospace; }}
h1 {{ color: gold; }}
</style>
</head>
<body>
<h1>Autogenesis Identity Report</h1>
<p><strong>Fingerprint:</strong> {fingerprint}</p>
<p><strong>Files:</strong> {file_count}</p>
<p><strong>Total Bytes:</strong> {total_bytes}</p>
<p><strong>Max Depth:</strong> {max_depth}</p>
<p><strong>Entropy Score:</strong> {entropy}</p>
<p>Generated: {datetime.utcnow().isoformat()} UTC</p>
</body>
</html>
"""
    (root / "identity_report.html").write_text(html)

    cert = f"""
WEIRDISMS STRUCTURAL IDENTITY CERTIFICATE
------------------------------------------
Fingerprint: {fingerprint}
Files: {file_count}
Total Bytes: {total_bytes}
Max Depth: {max_depth}
Entropy: {entropy}

Any modification invalidates this certificate.
"""
    (root / "IDENTITY_CERTIFICATE.txt").write_text(cert)

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    data = compute_repo_data(root)
    generate_outputs(root, data)
    print("Autogenesis DELUXE complete.")
