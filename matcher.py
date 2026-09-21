def rank_providers(providers):
    return sorted(
        providers,
        key=lambda provider: (
            not provider.tricare_prime,
            not provider.tricare_select,
            not provider.pediatric,
            provider.name.lower(),
        ),
    )
