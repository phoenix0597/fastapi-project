import pytest
from httpx import AsyncClient
from datetime import datetime


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    # *[(4, "2025-08-12", "2025-08-22", 201)] * 8,
    (4, "2025-08-12", "2025-08-22", 3, 201),
    (4, "2025-08-12", "2025-08-22", 4, 201),
    (4, "2025-08-12", "2025-08-22", 5, 201),
    (4, "2025-08-12", "2025-08-22", 6, 201),
    (4, "2025-08-12", "2025-08-22", 7, 201),
    (4, "2025-08-12", "2025-08-22", 8, 201),
    (4, "2025-08-12", "2025-08-22", 9, 201),
    (4, "2025-08-12", "2025-08-22", 10, 201),
    (4, "2025-08-12", "2025-08-22", 10, 409),
    (4, "2025-08-12", "2025-08-22", 10, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms, status_code,
                                   authenticated_async_client: AsyncClient):
    # headers = {"Authorization": f"Bearer {authenticated_async_client.cookies['booking_access_token']}"}
    response = await authenticated_async_client.post("/bookings/", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
        # }, headers=headers)
    })

    # print(f"Request URL: {response.request.url}")
    # print(f"Request method: {response.request.method}")
    # print(f"Request headers: {response.request.headers}")
    # print(f"Request body: {response.request.content}")
    # print(f"Response status: {response.status_code}")
    # print(f"Response headers: {response.headers}")
    # print(f"Response body: {response.text}")
    assert response.status_code == status_code

    response = await authenticated_async_client.get("/bookings/")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_all_bookings(authenticated_async_client):
    # Шаг 1: Получаем все бронирования
    response = await authenticated_async_client.get("/bookings/")
    assert response.status_code == 200
    bookings = response.json()

    # Убедимся, что у нас есть бронирования для удаления
    assert isinstance(bookings, list)
    assert len(bookings) > 0

    # Шаг 2: Удаляем каждое бронирование по его ID
    for booking in bookings:
        booking_id = booking['id']
        delete_response = await authenticated_async_client.delete(f"/bookings/{booking_id}")
        assert delete_response.status_code == 204

    # Шаг 3: Проверяем, что все бронирования удалены
    final_response = await authenticated_async_client.get("/bookings/")
    assert final_response.status_code == 200
    remaining_bookings = final_response.json()
    assert len(remaining_bookings) == 0
