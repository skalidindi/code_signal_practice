"""
code signal: banking system
Requirements
Your task is to implement a simplified version of a banking system. Plan your design according to the level
specifications below:
• Level 1: The banking system should support creating new accounts and depositing money into and withdrawing/paying
money from accounts.
• Level 2: The banking system should support ranking accounts based on the total value of transactions.
• Level 3: The banking system should support scheduling transfers and checking the scheduled transfer status.
• Level 4: The banking system should support merging two accounts while retaining the balances and transaction
histories of the original accounts.
To move to the next level, you should pass all the tests at the current level.
Note
You will receive a list of queries to the system, and the final output should be an array of strings representing
the returned values of all queries. Each query will only call one operation.
All queries will have a timestamp parameter — a string field timestamp in milliseconds. It is
guaranteed that all timestamps are unique and are in a range from 1 to 10^9.
Queries will be given in the order of strictly increasing timestamps.

Level 1:
1, CREATE_ACCOUNT<timestamp><accountId>, returns true if not present and create account, false otherwise
2, DEPOSIT <timestamp><accountId><amount>, deposit given amount of money to the specific account. returns a string
representing total money in the account (balance). If account does not exist, return empty string.
3, PAY <timestamp> <accountId> <amount>, withdraw from the account. returns a string representing account balance
after processing the query. If account does not exist or insufficient fund, return empty string.

Level 2:
The banking system should support ranking accounts based on total number of transactions.
1, TOP_ACTIVITY <timestamp> <n> return the top n accounts with the highest total value of transactions in descending
order. A string representing an array of accounts and transaction values in this format
"<accountId1>(<transactionValue1>)".
* Total value of transactions is defined as the sum of all transactions for an account (regardless of how the
 transaction affects account balance), including the amount of money deposited, withdrawn,
 and/or successfully transferred (transfers will be introduced on level 3, so you can ignore them for now).
* If less than n accounts exist in the system, return all active accounts (in the described format).

Level 3
The banking system should allow scheduling payments and checking the status of scheduled payments.
1, TRANSFER <timestamp> <sourceAccountId> ‹targetAccountId> <amount> - should initiate a transfer between accounts.
The given amount of money should be withdrawn from the source account sourceAccountId and held until the transfer
 is accepted by the target account targetAccountId, or until the transfer expires. The withheld money is added
 back to the source account's balance if the transfer expires. After the query is processed:
• Returns an empty string if sourceAccountId is equal to targetAccountId.
• Returns an empty string if sourceAccountId or targetAccountId doesn't exist.
• Returns an empty string if the source account sourceAccountId has insufficient funds to perform the transfer.
• The expiration period is 24 hours, which is equal to 24 • 60 • 60 • 1000 = 86400000 milliseconds.
A transfer expires at the beginning of the next millisecond after the expiration period ends.
• A valid TransFer should return a string containing a unique transfer ID in the following format
"transfer[ordinal number of the transfer]", e.g., "transfer1","transfer2", etc.
• For transfers, transaction history for source and target accounts is only updated when the transfer is accepted.
• Transfers count toward the total value of transactions of both source and target accounts.

2, ACCEPT_TRANSFER ‹timestamp> <accountId> <transferId> - Should accept the transfer with the given transferId.
• Returns True if the transfer was successfully accepted or False otherwise.
• Returns False if a transfer with transferId does not exist, was already accepted, or has expired.
• Returns False if the given accountId was not the target account for the transfer.

pay (self, timestamp: int, account_id: str, amount: int) -> str | None
- Should withdraw the given amount of money from the specified account. All withdraw transactions provide a 2% cashback
 - 2% of the withdrawn amount (rounded down to the nearest integer) will be refunded to the account 24 hours after
  the withdrawal. If the withdrawal is successful (i.e., the account holds sufficient funds to withdraw
   the given amount), returns a string with a unique identifier for the payment transaction in this format:
    "payment(ordinal number of withdraws from all accounts]" -e.g., "payment1", "payment2", etc.
Additional conditions:
• Returns None if account_id doesn't exist.
• Returns None if account_id has insufficient funds to perform the payment.
• top_spenders should now also account for the total amount of money withdrawn from accounts.
• The waiting period for cashback is 24 hours, equal to 24 * 60 * 60 * 1000 = 86400000 milliseconds
  (the unit for timestamps). So, cashback will be processed at timestamp, timestamp + 86400000 .
• When it's time to process cashback for a withdrawal, the amount must be refunded to the account before any other
  transactions are performed at the relevant timestamp.

get_payment_status (self, timestamp: int, account_id: str, payment: str) -> str | None -
Should return the status of the payment transaction for the given payment.
Specifically:
• Returns None if account_id doesn't exist.
• Returns None if the given payment doesn't exist for the specified account.
• Returns None if the payment transaction was for an account with a different identifier from account_id
• Returns a string representing the payment status: "IN_PROGRESS" or "CASHBACK_RECEIVED".

The system should allow scheduling payments and checking the status of scheduled payments.
• SCHEDULE_PAYMENT < timestamp> < accountId> ‹amount > ‹delay> - should schedule a payment which will be performed
at timestamp + delay. Returns a string with a unique identifier for the scheduled payment in the following format:
"payment [ordinal number of the scheduled payment across all accounts]" - e.g.,
"payment1", "payment2", etc. If account id doesn't exist, should return an empty string. The payment is skipped if the
specified account has insufficient funds when the payment is performed.
Additional conditions:
• Successful payments should be considered outgoing transactions and included when ranking accounts using the
TOP_SPENDERS operation.
• Scheduled payments should be processed before any other transactions at the given timestamp.
• If an account needs to perform several scheduled payments simultaneously, they should be processed in order
 of creation - e.g., "payment1" should be processed before "payment2"

CANCEL_PAYMENT < timestamp> <accountId> <paymentId> - should cancel the scheduled payment with paymentId.
Returns "true" if the scheduled payment is successfully canceled. If payment id does not exist or was already canceled,
 or if account id is different from the source account for the scheduled payment, returns
"false" . Note that scheduled payments must be performed before any CANCEL_PAYMENT operations at the given timestamp.


Level 4

The banking system should support merging two accounts while retaining both accounts' balance and transaction histories

merge_accounts (self, timestamp: int, account_id_1: str, account_id_2: str) -> bool
- Should merge account_id_2 into the account_id_1.
Returns True if accounts were successfully merged, or False otherwise.
Specifically:
• Returns False If account_id_1 is equal to account_id_2.
• Returns False if account_id_1 or account_id_2 doesn't exist.
• All pending cashback refunds for account_id_2 should still be processed, but refunded to account_id_1 instead.
• After the merge, it must be possible to check the status of payment transactions for account_id_2 with payment
identifiers by replacing account_id_2 with account_id_1
• The balance of account_sa_2 should be added to the balance for account_id_1
• top_spenders operations should recognize merged accounts - the total outgoing transactions for merged accounts
should be the sum of all money transferred and/or withdrawn in both accounts.
• account_id_2 should be removed from the system after the merge.

get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None
 - Should return the total amount of money in the account account_id at the given timestamp time_at.
 If the specified account did not exist at a given time time_at, returns None
• If queries have been processed at timestamp time_at, get_balance must reflect the account balance after the query
has been processed.
• If the account was merged into another account, the merged account should inherit its balance history.

Note: Not clear what to return for a get_balance query of a deleted account in the merge. This version returns
the balance by tracing to the target account in the merge.
"""

from enum import Enum
from math import floor

from sortedcontainers import SortedList


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"
    CASHBACK = "CASHBACK"
    PAYMENT = "PAYMENT"


class PaymentType(Enum):
    CASHBACK = "cashback"
    SCHEDULED = "default"


MILLISECONDS_IN_1_DAY = 24 * 60 * 60 * 1000


class Transaction:
    def __init__(self, ts: int, type: TransactionType, amount: int) -> None:
        self.type = type
        self.amount = amount
        self.ts = ts


class Transfer:
    def __init__(self, ts: int, source_account_id: str, target_account_id: str, amount: int) -> None:
        self.ts = ts
        self.source_account_id = source_account_id
        self.target_account_id = target_account_id
        self.amount = amount


class Payment:
    def __init__(
        self, ts: int, account_id: str, payment_id: str, amount: int, type: PaymentType = PaymentType.SCHEDULED
    ) -> None:
        self.ts = ts
        self.payment_id = payment_id
        self.account_id = account_id
        self.amount = amount
        self.type = type


class Account:
    def __init__(self, ts: int, account_id: str) -> None:
        self.account_id = account_id
        self.balance = 0
        self.held = 0
        self.creation_time = ts
        self.transactions: SortedList = SortedList(key=lambda x: x.ts)
        self.total_transaction_value = 0
        self.total_withdrawn = 0

    def deposit(self, ts: int, amount: int) -> str:
        if amount <= 0:
            return ""

        self.transactions.append(Transaction(ts, TransactionType.DEPOSIT, amount))
        self.total_transaction_value += amount
        self.balance += amount

        return str(self.balance)

    def withdraw(self, ts: int, amount: int) -> str | None:
        if not self.has_enough_balance(amount):
            return None

        self.transactions.append(Transaction(ts, TransactionType.WITHDRAW, -amount))
        self.total_transaction_value += amount
        self.balance -= amount
        self.total_withdrawn += amount

        return str(self.balance)

    def has_enough_balance(self, amount: int) -> bool:
        return self.balance - self.held - amount >= 0


class Bank:
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = dict()
        self.TRANSFER_EXPIRATION_PERIOD = MILLISECONDS_IN_1_DAY
        self.CASHBACK_WAITING_PERIOD = MILLISECONDS_IN_1_DAY
        self.CASHBACK_PERCENTAGE = 0.02

        self.transfer_ordinal = 0
        self.pending_transfers: dict[int, Transfer] = {}

        self.payment_ordinal = 0
        self.scheduled_payments: dict[str, Payment] = {}

        self.completed_payments: dict[str, Payment] = {}

        self.account_merges: dict[str, str] = {}

    def create_account(self, ts: str, account_id: str) -> bool:
        if account_id in self.accounts:
            return False

        self.accounts[account_id] = Account(parse_str_to_int(ts), account_id)
        return True

    def deposit(self, ts: str, account_id: str, amount: int) -> str:
        self._process_scheduled_payments(parse_str_to_int(ts))
        if account_id not in self.accounts:
            return ""

        account = self.accounts[account_id]

        return account.deposit(parse_str_to_int(ts), amount)

    def pay(self, ts: int, account_id: str, amount: int) -> str | None:
        self._expire_transfers(ts)
        self._process_scheduled_payments(ts)
        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]

        res = account.withdraw(ts, amount)
        if res is None:
            return None

        cashback_amount = floor(amount * self.CASHBACK_PERCENTAGE)
        self.payment_ordinal += 1
        payment_id = f"payment{self.payment_ordinal}"
        self.scheduled_payments[payment_id] = Payment(
            ts + self.CASHBACK_WAITING_PERIOD, account_id, payment_id, cashback_amount, PaymentType.CASHBACK
        )
        return payment_id

    def transfer(self, ts: str, source_account_id: str, target_account_id: str, amount: int):
        self._expire_transfers(parse_str_to_int(ts))
        self._process_scheduled_payments(parse_str_to_int(ts))
        if (
            source_account_id == target_account_id
            or source_account_id not in self.accounts
            or target_account_id not in self.accounts
        ):
            return ""

        source_account = self.accounts[source_account_id]
        if not source_account.has_enough_balance(amount):
            return ""

        self.transfer_ordinal += 1
        self.pending_transfers[self.transfer_ordinal] = Transfer(
            parse_str_to_int(ts), source_account_id, target_account_id, amount
        )
        source_account = self.accounts[source_account_id]
        source_account.held += amount

        return f"transfer{self.transfer_ordinal}"

    def _expire_transfers(self, ts: int) -> None:
        expired_ids = []
        for id, transfer in self.pending_transfers.items():
            if ts - transfer.ts > self.TRANSFER_EXPIRATION_PERIOD:
                source_account = self.accounts[transfer.source_account_id]
                source_account.held -= transfer.amount
                expired_ids.append(id)

        for id in expired_ids:
            del self.pending_transfers[id]

    def accept_transfer(self, ts: str, account_id: str, transfer_id: str) -> bool:
        self._process_scheduled_payments(parse_str_to_int(ts))
        parsed_numeric_transfer_id = parse_str_to_int(transfer_id[len("transfer") :])
        parsed_numeric_ts = parse_str_to_int(ts)
        self._expire_transfers(parsed_numeric_ts)

        if parsed_numeric_transfer_id not in self.pending_transfers:
            return False

        pending_transfer = self.pending_transfers[parsed_numeric_transfer_id]
        if pending_transfer.target_account_id != account_id:
            return False

        source_account = self.accounts[pending_transfer.source_account_id]
        target_account = self.accounts[pending_transfer.target_account_id]

        source_account.held -= pending_transfer.amount
        source_account.balance -= pending_transfer.amount
        source_account.transactions.append(
            Transaction(parse_str_to_int(ts), TransactionType.TRANSFER_OUT, -pending_transfer.amount)
        )
        source_account.total_transaction_value += pending_transfer.amount
        target_account.balance += pending_transfer.amount
        target_account.transactions.append(
            Transaction(parse_str_to_int(ts), TransactionType.TRANSFER_IN, pending_transfer.amount)
        )
        target_account.total_transaction_value += pending_transfer.amount
        del self.pending_transfers[parsed_numeric_transfer_id]

        return True

    def get_payment_status(self, ts: int, account_id: str, payment_id: str) -> str | None:
        resolved_account_id = self.account_merges.get(account_id, account_id)
        if resolved_account_id not in self.accounts or (
            payment_id not in self.scheduled_payments and payment_id not in self.completed_payments
        ):
            return None

        if payment_id in self.completed_payments:
            completed_payment = self.completed_payments[payment_id]
            if completed_payment.account_id != resolved_account_id:
                return None
            if completed_payment.type == "cashback":
                return "CASHBACK_RECEIVED"

            return None
        else:
            payment = self.scheduled_payments[payment_id]
            if payment.account_id != resolved_account_id:
                return None

            return "IN_PROGRESS"

    def schedule_payment(self, ts: str, account_id: str, amount: int, delay: int) -> str:
        if account_id not in self.accounts:
            return ""

        self.payment_ordinal += 1
        payment_id = f"payment{self.payment_ordinal}"
        self.scheduled_payments[payment_id] = Payment(
            parse_str_to_int(ts) + delay, account_id, payment_id, amount, PaymentType.SCHEDULED
        )

        return payment_id

    def cancel_payment(self, ts: str, account_id: str, payment_id: str) -> bool:
        self._process_scheduled_payments(parse_str_to_int(ts))
        if payment_id not in self.scheduled_payments:
            return False

        payment = self.scheduled_payments[payment_id]
        if payment.account_id != account_id:
            return False

        del self.scheduled_payments[payment_id]
        return True

    def _process_scheduled_payments(self, ts: int) -> None:
        sorted_scheduled_payments = sorted(
            self.scheduled_payments.values(), key=lambda x: (x.ts, int(x.payment_id[len("payment") :]))
        )
        parsed_payment_ids = []
        for payment in sorted_scheduled_payments:
            if payment.ts > ts:
                break
            elif payment.account_id in self.accounts:
                account = self.accounts[payment.account_id]
                if payment.type == TransactionType.CASHBACK:
                    account.balance += payment.amount
                    account.transactions.append(Transaction(ts, TransactionType.CASHBACK, payment.amount))
                elif account.has_enough_balance(payment.amount):
                    account.balance -= payment.amount
                    account.transactions.append(Transaction(ts, TransactionType.PAYMENT, -payment.amount))
                    account.total_transaction_value += payment.amount
                    account.total_withdrawn += payment.amount

                parsed_payment_ids.append(payment.payment_id)
                self.completed_payments[payment.payment_id] = payment

        for id in parsed_payment_ids:
            del self.scheduled_payments[id]

    def get_top_activity_accounts(self, ts: str, n: int) -> str:
        accts = list(self.accounts.values())
        accts.sort(key=lambda x: x.total_transaction_value, reverse=True)

        accts = accts[:n]

        return ", ".join(f"{acc.account_id}({acc.total_transaction_value})" for acc in accts)

    def top_spenders(self, ts: str, n: int):
        accts = list(self.accounts.values())
        accts.sort(key=lambda x: x.total_withdrawn, reverse=True)

        accts = accts[:n]
        return ", ".join(f"{acc.account_id}({acc.total_withdrawn})" for acc in accts)

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        if account_id_1 == account_id_2 or account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False

        account1 = self.accounts[account_id_1]
        account2 = self.accounts[account_id_2]

        account1.balance += account2.balance
        account1.held = account1.held + account2.held
        account1.transactions.update(account2.transactions)
        account1.total_transaction_value = account1.total_transaction_value + account2.total_transaction_value
        account1.total_withdrawn = account1.total_withdrawn + account2.total_withdrawn

        for payment in self.scheduled_payments.values():
            if payment.account_id == account_id_2:
                payment.account_id = account_id_1

        for payment in self.completed_payments.values():
            if payment.account_id == account_id_2:
                payment.account_id = account_id_1

        self.account_merges[account_id_2] = account_id_1
        del self.accounts[account_id_2]
        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        resolved_account_id = self.account_merges.get(account_id, account_id)

        if resolved_account_id not in self.accounts:
            return None

        account = self.accounts[resolved_account_id]
        if account.creation_time > time_at:
            return None

        balance = 0
        for acct_transaction in account.transactions:
            tx: Transaction = acct_transaction
            if tx.ts > time_at:
                break

            balance += tx.amount

        return balance


def parse_str_to_int(ts: str) -> int:
    try:
        int_ts = int(ts)
        return int_ts
    except Exception as e:
        raise Exception(f"Unable to parse string input to int due to bad input: {e}") from e
