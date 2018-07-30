import pytest
from pages.book_salons import BookSalons
from pages.availability import Availability
from pages.signin import Signin
from pages.register import Register
from config import BOOK_SALONS_URL


# @pytest.mark.skip(reason="uncomment to skip me")
def test_book_single_signup(driver, logger, config):

    """
        test scenario:
        open book salon demo
        book an appointment
        submit register form with an incorrect too short password
        submit register form - successfully logged in and land on confirm page
    """

    salons = BookSalons(logger, driver, config)

    email = "{}@gmail.com".format(salons.time_in_ms)
    password = config.get("password")
    user_name = "Phorest QA"

    salons.open_url(BOOK_SALONS_URL)

    salons.click_service_by_idx(2, 2, 1)

    salons.click_book_now()

    salons.select_btn_book_now_modal()

    availability = Availability(logger, driver, config)

    availability.click_available_time()

    signin = Signin(logger, driver, config)

    signin.click_btn_no_account()

    # register

    reg = Register(logger, driver, config)

    reg.enter_name(user_name)
    reg.enter_email(email)
    reg.enter_mobile("0851" + reg.get_random_str_number(6))

    # validate password
    reg.enter_password("134")
    reg.click_btn_signup()
    assert reg.get_form_error() == "Passwords must be a minimum of 8 characters"

    # ok password
    reg.enter_password(password)
    reg.click_btn_signup()

    reg.ensure_no_form_error()

    reg.ensure_confirm_active_breadcrumb()


def test_book_multiple_services_login(driver, logger, config):

    """
        test scenario:
        open book salon demo
        book an appointment for multiple services
        login as an existing user with an incorrect password ( too short )
        login successfully
        ensure that logged in
        ensure that user lands on confirm page
    """

    salons = BookSalons(logger, driver, config)

    email = config.get("user-reg-01")
    password = config.get("password")

    salons.open_url(BOOK_SALONS_URL)

    salons.click_service_by_idx(2, 3, 1)

    salons.click_book_now()

    salons.select_btn_add_more_services_modal()

    salons.click_service_by_idx(2, 3, 2)

    salons.click_book_now()

    salons.select_btn_book_now_modal()

    availability = Availability(logger, driver, config)

    availability.click_available_time()

    signin = Signin(logger, driver, config)

    signin.enter_email(email)
    signin.enter_password("134")

    signin.click_btn_login(False)

    # validate password
    assert signin.get_form_error() == "Passwords must be a minimum of 8 characters"

    # ok password
    signin.enter_password(password)
    signin.click_btn_login(True)

    signin.ensure_no_form_error()

    signin.ensure_confirm_active_breadcrumb()
