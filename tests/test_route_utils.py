from services.route_utils import sample_route_coordinates


def test_sample_route_coordinates_returns_start_middle_end():

    coordinates = [
        [-95.3698, 29.7604],
        [-95.8000, 29.8500],
        [-96.5000, 30.0000],
        [-97.0000, 30.1000],
        [-97.7431, 30.2672]
    ]

    result = sample_route_coordinates(
        coordinates,
        max_points=3
    )

    assert result == [
        coordinates[0],
        coordinates[2],
        coordinates[4]
    ]

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