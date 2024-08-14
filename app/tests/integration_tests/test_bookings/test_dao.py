from datetime import date, datetime

from app.bookings.dao import BookingDAO


# Adding new booking
async def test_add_and_get_booking():
    # add new booking
    new_booking = await BookingDAO.add(
        2,
        2,
        # date_from=date(2023, 6, 15),
        # date_to=date(2023, 6, 20))
        date_from=datetime.strptime("2024-08-12", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-08-22", "%Y-%m-%d"),
    )

    print(new_booking)
    # Check that new booking was added successfully, and it has the room_id and user_id set when it was created
    assert new_booking.room_id == 2
    assert new_booking.user_id == 2

    #  Check that new booking was added successfully
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None

    # user_id = new_booking.user_id
    new_booking_id = new_booking.id
    # Deleting created booking
    await BookingDAO.delete(new_booking_id)

    # Check that new booking was deleted successfully
    new_booking = await BookingDAO.find_by_id(new_booking_id)
    assert new_booking is None
