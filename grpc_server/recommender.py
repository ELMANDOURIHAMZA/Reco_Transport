def recommend_transport(distance_km):
    """
    Recommande le moyen de transport le plus adapté basé sur la distance réelle.
    
    Args:
        distance_km: Distance du trajet en kilomètres
    
    Returns:
        str: Mode de transport recommandé
    """
    if distance_km <= 0:
        return "Aucun trajet disponible"
    
    # Recommandations basées sur la distance réelle en km
    # Taxi: trajets courts (0-3 km) - rapide et direct
    if distance_km <= 3:
        return "Taxi"
    # Tramway: trajets moyens (3-8 km) - équilibre coût/efficacité
    elif distance_km <= 8:
        return "Tramway"
    # Bus: trajets longs (> 8 km) - économique pour longues distances
    else:
        return "Bus"
