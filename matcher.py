def score_provider(provider):
    score = 0

    if provider.tricare_prime:
        score += 10
    if provider.tricare_select:
        score += 5
    if provider.pediatric:
        score += 7

    # penalty logic placeholder (expand later)
    if not provider.tricare_prime and not provider.tricare_select:
        score -= 5

    return score


def rank_providers(providers):
    return sorted(providers, key=score_provider, reverse=True)
