from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"
    

class ExpiredTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token"


class TokenIsAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token is absent or invalid"


class TokenIncorrectFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "No rooms available for booking"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Date from cannot be after date to"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Cannot book hotel for long period"