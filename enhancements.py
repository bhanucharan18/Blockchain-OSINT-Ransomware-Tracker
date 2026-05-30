def calculate_risk(ransomware_match, hops, mixer_used, darkweb):
    score = 0

    if ransomware_match:
        score += 40
    if hops >= 3:
        score += 20
    if mixer_used:
        score += 25
    if "Mentioned" in darkweb:
        score += 15

    return min(score, 100)


def detect_mixer(path):
    for node in path:
        if "Mixer" in node:
            return True
    return False
