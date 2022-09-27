import json
import random

from faker import Faker
import pytest


fake = Faker()


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


def test_v1_event(flask_client, type, amount, user_id, t):
    @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    def success(flask_client, type, amount, user_id, t):
        response_raw = flask_client.post(
            "/v1/event/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "amount": amount,
                    "t": t,
                    "type": type,
                    "user_id": user_id,
                }
            ),
        )

        response = json.loads(response_raw.data.decode("utf-8"))

        assert response_raw.status_code == 200

        assert response["alert"] is False
        assert not response["alert_codes"]
        assert response["user_id"] == str(user_id)

    def failure_no_user_id_in_request(flask_client, type, amount, t):
        response = flask_client.post(
            "/v1/event/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "amount": amount,
                    "t": t,
                    "type": type,
                }
            ),
        )

        assert response.status_code == 400

        assert b'"user_id is required"' in response.data

    # Call the above test functions
    # @pytest.mark.skip(reason="Need to mock out sqlalchemy.orm.Session")
    # success(flask_client, type, amount, user_id, t)
    failure_no_user_id_in_request(flask_client, type, amount, t)
