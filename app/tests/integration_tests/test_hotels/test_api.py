import pytest


@pytest.mark.parametrize(
    "location, date_from_key, date_to_key, expected_status, expected_detail",
    [
        ("Алтай", "today", "today", 400, "Date from cannot be equal or after date to"),
        ("Алтай", "today", "date_far_later", 400, "Cannot book hotel for long (more than 30 days) period"),
        ("Алтай", "date_far_later", "today", 400, "Date from cannot be equal or after date to"),
        ("Алтай", "date_before_today", "date_soon", 400, "Cannot book hotel before today"),
        ("Алтай", "date_soon", "date_later", 200, None),
    ]
)
async def test_get_hotels_by_location_and_time(
        async_client, setup_dates, location, date_from_key, date_to_key, expected_status, expected_detail
):
    """Параметризированный тест для проверки разных сценариев запроса"""
    date_from = setup_dates[date_from_key]
    date_to = setup_dates[date_to_key]

    response = await async_client.get(f"/hotels/{location}/search", params={"date_from": date_from, "date_to": date_to})

    assert response.status_code == expected_status

    if expected_detail:
        assert expected_detail in response.text
    else:
        assert isinstance(response.json(), list)
