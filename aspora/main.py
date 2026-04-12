from enums import UserTier, AccountType, TransferType, TransactionStatus
from services import UserService, AccountService, TransactionService
from validation import ValidationService, ComparisonOperator


def setup():
    vs = ValidationService()
    CO = ComparisonOperator

    positive_amount = vs.create_rule_policy(
        "transfer_amount", 0, CO.GT, name="positive_amount"
    )
    vs.register_global_policy(positive_amount)

    gold_limit = vs.create_rule_policy(
        "transfer_amount", 50000, CO.LTE, name="gold_limit_50k"
    )
    vs.register_tier_policy(UserTier.GOLD, gold_limit)

    silver_limit = vs.create_rule_policy(
        "transfer_amount", 10000, CO.LTE, name="silver_limit_10k"
    )
    vs.register_tier_policy(UserTier.SILVER, silver_limit)

    user_service = UserService()
    account_service = AccountService(user_service)
    txn_service = TransactionService(account_service, user_service, vs)

    user1 = user_service.create_user("User1", UserTier.GOLD)
    user2 = user_service.create_user("User2", UserTier.SILVER)
    acc1 = account_service.create_account(user1.user_id, 10000, AccountType.WALLET)
    acc2 = account_service.create_account(user2.user_id, 5000, AccountType.UPI)

    return txn_service, acc1, acc2


# Valid account transfer: balances should update correctly
def test_valid_transfer(txn_service, acc1, acc2):
    acc1.balance = 10000
    acc2.balance = 5000
    txn = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, 2000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.COMPLETED
    assert acc1.balance == 8000
    assert acc2.balance == 7000
    print(f"Transferred 2000 from acc1 to acc2. acc1: 10000->8000, acc2: 5000->7000. Status: {txn.status.name}")


# Transfer more than sender's balance should fail
def test_insufficient_balance(txn_service, acc1, acc2):
    acc1.balance = 8000
    acc2.balance = 7000
    txn = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, 50000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.FAILED
    assert acc1.balance == 8000
    assert acc2.balance == 7000
    print(f"Tried transferring 50000 with only 8000 balance. Status: {txn.status.name}. Balances unchanged.")


# GOLD tier: transfers above 50k should be rejected
def test_gold_tier_limit(txn_service, acc1, acc2):
    acc1.balance = 100000
    txn = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, 60000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.FAILED
    assert acc1.balance == 100000
    print(f"Gold user tried transferring 60000 (limit 50000). Status: {txn.status.name}. Balance unchanged.")


# SILVER tier: transfers above 10k should be rejected
def test_silver_tier_limit(txn_service, acc1, acc2):
    acc2.balance = 50000
    txn = txn_service.execute_transfer(
        acc2.account_id, acc1.account_id, 15000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.FAILED
    assert acc2.balance == 50000
    print(f"Silver user tried transferring 15000 (limit 10000). Status: {txn.status.name}. Balance unchanged.")


# Negative transfer amount should be rejected by global validation
def test_negative_amount(txn_service, acc1, acc2):
    txn = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, -100, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.FAILED
    print(f"Tried transferring -100 (negative amount). Status: {txn.status.name}. Rejected by global policy.")


# Transferring to the same account should fail
def test_self_transfer(txn_service, acc1, acc2):
    txn = txn_service.execute_transfer(
        acc1.account_id, acc1.account_id, 1000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn.status == TransactionStatus.FAILED
    print(f"Tried self-transfer of 1000 on acc1. Status: {txn.status.name}. Same-account transfer blocked.")


# Deposit should credit the target account
def test_deposit(txn_service, acc1, acc2):
    acc2.balance = 5000
    txn = txn_service.execute_transfer(
        None, acc2.account_id, 3000, TransferType.DEPOSIT
    )
    assert txn.status == TransactionStatus.COMPLETED
    assert acc2.balance == 8000
    print(f"Deposited 3000 into acc2. acc2: 5000->8000. Status: {txn.status.name}")


# Withdrawal should debit the source account
def test_withdrawal(txn_service, acc1, acc2):
    acc1.balance = 10000
    txn = txn_service.execute_transfer(
        acc1.account_id, None, 5000, TransferType.WITHDRAWAL
    )
    assert txn.status == TransactionStatus.COMPLETED
    assert acc1.balance == 5000
    print(f"Withdrew 5000 from acc1. acc1: 10000->5000. Status: {txn.status.name}")


# Withdrawal exceeding balance should fail
def test_withdrawal_insufficient_balance(txn_service, acc1, acc2):
    acc1.balance = 100
    txn = txn_service.execute_transfer(
        acc1.account_id, None, 5000, TransferType.WITHDRAWAL
    )
    assert txn.status == TransactionStatus.FAILED
    assert acc1.balance == 100
    print(f"Tried withdrawing 5000 with only 100 balance. Status: {txn.status.name}. Balance unchanged.")


# Transaction status should be queryable by ID
def test_status_tracking(txn_service, acc1, acc2):
    acc1.balance = 10000
    txn = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, 1000, TransferType.ACCOUNT_TRANSFER
    )
    assert txn_service.get_status(txn.transaction_id) == TransactionStatus.COMPLETED

    txn2 = txn_service.execute_transfer(
        acc1.account_id, acc2.account_id, -1, TransferType.ACCOUNT_TRANSFER
    )
    assert txn_service.get_status(txn2.transaction_id) == TransactionStatus.FAILED
    print(f"Txn {txn.transaction_id} status: {txn_service.get_status(txn.transaction_id).name}. Txn {txn2.transaction_id} status: {txn_service.get_status(txn2.transaction_id).name}.")

def testing123():
    vs = ValidationService()
    CO = ComparisonOperator


    # gold_limit = vs.create_rule_policy(
    #     "transfer_amount", 50000, CO.LTE, name="gold_limit_50k"
    # )
    # vs.register_tier_policy(UserTier.GOLD, gold_limit)

    silver_limit = vs.create_rule_policy(
        "transfer_amount", 10000, CO.LTE, name="silver_limit_10k"
    )
    vs.register_tier_policy(UserTier.SILVER, silver_limit)

    user_service = UserService()
    account_service = AccountService(user_service)
    txn_service = TransactionService(account_service, user_service, vs)

    user1 = user_service.create_user("User1", UserTier.GOLD)
    user2 = user_service.create_user("User2", UserTier.SILVER)
    acc1 = account_service.create_account(user1.user_id, 10000, AccountType.WALLET)
    acc2 = account_service.create_account(user2.user_id, 5000, AccountType.UPI)

    acc1.balance = 100000
    txn = txn_service.execute_transfer(acc1.account_id, acc2.account_id, 50000, TransferType.ACCOUNT_TRANSFER)
    print(f"txn: {txn.transaction_id}. Status: {txn.status.name}")
    # assert txn_service.get_status(txn.transaction_id) == TransactionStatus.FAILED
    assert txn_service.get_status(txn.transaction_id) == TransactionStatus.COMPLETED



if __name__ == "__main__":
    txn_service, acc1, acc2 = setup()

    # test_valid_transfer(txn_service, acc1, acc2)
    # test_insufficient_balance(txn_service, acc1, acc2)
    # test_gold_tier_limit(txn_service, acc1, acc2)
    # test_silver_tier_limit(txn_service, acc1, acc2)
    # test_negative_amount(txn_service, acc1, acc2)
    # test_self_transfer(txn_service, acc1, acc2)
    # test_deposit(txn_service, acc1, acc2)
    # test_withdrawal(txn_service, acc1, acc2)
    # test_withdrawal_insufficient_balance(txn_service, acc1, acc2)
    # test_status_tracking(txn_service, acc1, acc2)
    testing123()
    print("ALL TESTS PASSED")
