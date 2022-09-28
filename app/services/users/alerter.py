from datetime import datetime, timedelta

from functools import cache, cached_property

from db import db_api


class Alerter:
    """
    Creates list of alert codes for a user based on their event history.
    """

    CODE_LAST_WITHDRAWL_WAS_OVER_THRESHOLD = 1100
    CODE_THREE_INCREASING_DEPOSITS = 300
    CODE_THREE_CONSEQUETIVE_WITHDRAWS = 30
    CODE_TOO_MANY_RECENT_DEPOSITS = 123
    DEPOSIT_ALERT_THRESHOLD = 200.00
    DEPOSIT_WINDOW_SECONDS = 30

    def __init__(self, user_id: str) -> None:
        self._user_id = user_id

    def alert_codes(self) -> list:
        """
        Returns list of alert codes for a user based on their event history.
        """
        codes = []

        if self._three_consequetive_withdraws():
            codes.append(self.CODE_THREE_CONSEQUETIVE_WITHDRAWS)

        if self._three_increasing_deposits():
            codes.append(self.CODE_THREE_INCREASING_DEPOSITS)

        if self._last_withdraw_was_over(amount=100.00):
            codes.append(self.CODE_LAST_WITHDRAWL_WAS_OVER_THRESHOLD)

        if self._too_many_recent_deposits():
            codes.append(self.CODE_TOO_MANY_RECENT_DEPOSITS)

        return codes

    # private

    def _deposits(self, limit: int = None) -> list:
        """
        Returns list of last deposits for a user.

        limit: number of deposits to return
        """
        return [
            event
            for event in self._events(limit=limit)
            if event.type == "deposit"
        ]

    @cached_property
    def _event_dao(self) -> db_api.EventDAO:
        """
        Returns event dao.
        """
        return db_api.EventDAO()

    @cache
    def _events(self, limit: int = None) -> list:
        """
        Returns list of events for a user (in desc order of created_at)

        limit: number of events to return
        """

        return self._event_dao.get_events(self._user_id, limit=limit)

    def _last_withdraw_was_over(self, amount: float = 100.00) -> bool:
        """
        Returns True if the last withdraw was over amount.

        amount: amount in dollars and cents to compare against
        """
        last_event = self._events()[0]

        return last_event.type == "withdraw" and last_event.amount > amount

    def _recent_deposits(self) -> list:
        """
        Returns list of recent deposits for a user.
        """

        last_deposits = self._deposits()
        timezone = last_deposits[0].created_at.tzinfo

        deposit_time_window = datetime.now(timezone) - timedelta(
            seconds=self.DEPOSIT_WINDOW_SECONDS
        )

        return [
            deposit
            for deposit in self._deposits()
            if deposit.created_at > deposit_time_window
        ]

    def _three_consequetive_withdraws(self) -> bool:
        """
        Returns True if the last three events were withdraws.
        """

        return all(event.type == "withdraw" for event in self._events()[:3])

    def _three_increasing_deposits(self) -> bool:
        """
        Returns True if the last three deposits were increasing in amount.
        """
        last_three_deposits = self._deposits()[:3]

        last_three_deposit_amounts = [
            deposit.amount for deposit in last_three_deposits
        ]

        return len(last_three_deposits) == 3 and all(
            i > j
            for i, j in zip(
                last_three_deposit_amounts, last_three_deposit_amounts[1:]
            )
        )

    def _too_many_recent_deposits(self) -> bool:
        """
        Returns True if there were more than DEPOSIT_ALERT_THRESHOLD
        number of deposits in the last DEPOSIT_WINDOW_SECONDS
        """

        return (
            sum(deposit.amount for deposit in self._recent_deposits())
            > self.DEPOSIT_ALERT_THRESHOLD
        )
