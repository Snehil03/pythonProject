from src.txn import find_duplicate_transactions
import pandas as pd
from pandas._testing import assert_frame_equal


# return transactions on the basis of sample data
def test_duplicate_txn():
    data = [{"id": 3, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:34:30.000Z'},
            {"id": 1, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:33:00.000Z'},
            {"id": 6, "sourceAccount": 'A', "targetAccount": 'C', "amount": 250, "category": 'other',
             "time": '2018-03-02T10:33:05.000Z'},
            {"id": 4, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:36:00.000Z'},
            {"id": 2, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:33:50.000Z'},
            {"id": 5, "sourceAccount": 'A', "targetAccount": 'C', "amount": 250, "category": 'other',
             "time": '2018-03-02T10:33:00.000Z'}]
    result = pd.DataFrame(find_duplicate_transactions(data))
    expected = [[{'id': 1,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:33:00.000Z'},
                 {'id': 2,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:33:50.000Z'},
                 {'id': 3,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:34:30.000Z'}],
                [{'id': 5,
                  'sourceAccount': 'A',
                  'targetAccount': 'C',
                  'amount': 250,
                  'category': 'other',
                  'time': '2018-03-02T10:33:00.000Z'},
                 {'id': 6,
                  'sourceAccount': 'A',
                  'targetAccount': 'C',
                  'amount': 250,
                  'category': 'other',
                  'time': '2018-03-02T10:33:05.000Z'}]]
    assert_frame_equal(result, pd.DataFrame(expected))


# boundary test cases for time stamp
def test_duplicate_boundary_txn():
    data = [{"id": 3, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:34:30.000Z'},
            {"id": 1, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:33:40.000Z'},
            {"id": 6, "sourceAccount": 'A', "targetAccount": 'C', "amount": 250, "category": 'other',
             "time": '2018-03-02T10:31:05.000Z'},
            {"id": 4, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:35:00.000Z'},
            {"id": 2, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:31:50.000Z'},
            {"id": 5, "sourceAccount": 'A', "targetAccount": 'C', "amount": 250, "category": 'other',
             "time": '2018-03-02T10:32:00.000Z'},
            {"id": 7, "sourceAccount": 'A', "targetAccount": 'D', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:37:00.000Z'}]
    result = pd.DataFrame(find_duplicate_transactions(data))
    expected = [[{'id': 1,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:33:40.000Z'},
                 {'id': 3,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:34:30.000Z'},
                 {'id': 4,
                  'sourceAccount': 'A',
                  'targetAccount': 'B',
                  'amount': 100,
                  'category': 'eating_out',
                  'time': '2018-03-02T10:35:00.000Z'}],
                [{'id': 6,
                  'sourceAccount': 'A',
                  'targetAccount': 'C',
                  'amount': 250,
                  'category': 'other',
                  'time': '2018-03-02T10:31:05.000Z'},
                 {'id': 5,
                  'sourceAccount': 'A',
                  'targetAccount': 'C',
                  'amount': 250,
                  'category': 'other',
                  'time': '2018-03-02T10:32:00.000Z'}]]
    assert_frame_equal(result, pd.DataFrame(expected))


# validated test case when multiple different transactions performed.
def test_no_duplicate_txn():
    data = [{"id": 3, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:34:30.000Z'},
            {"id": 7, "sourceAccount": 'A', "targetAccount": 'D', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:37:00.000Z'}]
    result = pd.DataFrame(find_duplicate_transactions(data))
    expected = []
    assert_frame_equal(result, pd.DataFrame(expected))


# validated test case when only test case performed.
def test_only_listed_txn():
    data = [{"id": 3, "sourceAccount": 'A', "targetAccount": 'B', "amount": 100, "category": 'eating_out',
             "time": '2018-03-02T10:34:30.000Z'}]
    result = pd.DataFrame(find_duplicate_transactions(data))
    expected = []
    assert_frame_equal(result, pd.DataFrame(expected))


