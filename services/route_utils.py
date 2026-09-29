def sample_route_coordinates(
    coordinates,
    max_points=3
):
    if not coordinates:
        return []

    if max_points <= 0:
        raise ValueError(
            "max_points must be greater than zero"
        )

    if len(coordinates) <= max_points:
        return coordinates

    if max_points == 1:
        return [coordinates[0]]

    step = (
        (len(coordinates) - 1)
        / (max_points - 1)
    )

    indexes = [
        round(i * step)
        for i in range(max_points)
    ]

    return [
        coordinates[index]
        for index in indexes
    ]