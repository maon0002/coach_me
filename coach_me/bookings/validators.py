from django.core import exceptions
# from coach_me.bookings.models import Company


def validate_if_string_is_alphanumeric(value):
    for character in value:
        if not (character == ' ' or character.isalnum()):
            raise exceptions.ValidationError("The text should contains only letters, numbers and spaces")
        break


def validate_phone_numbers_formatting(value):
    if not value.isdigit() or len(value) != 10:
        raise exceptions.ValidationError(
            "The phone number should contains only digits like '0888123456' and should be exactly 10 digits")
    # return str(value)

def validate_string_is_letters_only(value):
    if not value.isalpha():
        raise exceptions.ValidationError("You should use only letters!")


def validate_string_is_letters_and_hyphens_only(value):
    for character in value:
        # if not character == '-' or not character.isalpha():
        if not (character == '-' or character.isalpha()):
            raise exceptions.ValidationError("You should use only letters and hyphens!")
        break


# def validate_email_contain_correct_company_domain(value):
#     # if Booking.objects.filter(user=self.employee, start_time=self.start_time).exists():
#     #     raise ValidationError("This start time is already booked for the user.")
#     existing_domains = Company.objects.filter(company_domain__icontains=value).exists()
#     if not existing_domains:
#         raise exceptions.ValidationError(
#             "We can't find your company domain in our database, please contact our team for support or check if y")
