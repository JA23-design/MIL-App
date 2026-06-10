from services.geo import score_by_distance

def score_provider(provider, distance_km):
    score = 0

    # healthcare quality
    if provider.tricare_prime:
        score += 15
    if provider.tricare_select:
        score += 10
    if provider.pediatric:
        score += 8

    # distance factor (NEW)
    score += score_by_distance(distance_km)

    return score


def rank(items):
    return sorted(items, key=lambda x: x["score"], reverse=True)
