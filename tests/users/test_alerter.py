import random

import faker
import pytest

from app.services.users.alerter import Alerter as user_alerter


fake = faker.Faker()


@pytest.fixture
def amount():
    # Range from 1.00 to 100.00
    return round(random.uniform(1, 100), 2)


@pytest.fixture
def t():
    return fake.date_time_this_year().isoformat()


@pytest.fixture
def type():
    return random.choice(["deposit", "withdraw"])


@pytest.fixture
def user_id():
    return fake.uuid4()


class TestUserAlerter:
    @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    def test_alert_codes_no_previous_events(self, user_id):
        alerter = user_alerter(user_id)

        assert alerter.alert_codes() == []

    @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    def test_alert_codes_most_recent_withdraw_over_100(self, user_id):
        amount = 101.00

        alerter = user_alerter(user_id)

        assert alerter.alert_codes() == [1100]

    @pytest.mark.skip(
        reason="Need to mock out sqlalchemy.orm.Session / events"
    )
    def test_alert_codes_three_consequetive_withdraws(self, amount, user_id):
        alerter = user_alerter(user_id)

        assert alerter.alert_codes() == [30]

    @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    def test_alert_codes_three_consequetive_increasing_deposits(
        self, amount, user_id
    ):
        deposit_1_amount = amount
        deposit_2_amount = amount + 1
        deposit_3_amount = amount + 2

        alerter = user_alerter(user_id)

        assert alerter.alert_codes() == [300]

    @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    def test_alert_codes_too_many_recent_deposits(self, amount, user_id):
        alerter = user_alerter(user_id)

        assert alerter.alert_codes() == [123]
