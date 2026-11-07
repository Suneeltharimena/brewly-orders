# Tasks

Do them in order, one branch and one pull request each. For each one: read the code and tests first, write your plan, then direct the agent in small steps and check every step yourself.

## Task 1: customers are charged twice

**Report from the cafés:** "Customers say they paid twice for one coffee. It happens when the app is slow and they tap Pay again, and sometimes when nobody tapped twice at all."

- Find why, in `brewly_orders/orders.py`, and fix it.
- Done means: `tests/test_task1_double_charge.py` passes, every other test still passes, and one order is never charged twice, however often the request is retried.
- Before you accept the fix, break it on purpose and watch a task 1 test fail.

## Task 2: tell the customer when to collect

**Request from Brewly's operations lead:** "When an order is paid, show the customer how many minutes until it is ready."

The rule (practice data):

- Each drink takes one barista 1.5 minutes. Food comes from the counter and takes no barista time.
- Count the drinks in this order plus the drinks in orders at the **same café** that are paid but not yet collected.
- Share them between the baristas on shift (`baristas_on_shift` in `brewly_orders/cafes.py`).
- Round up to whole minutes, with a minimum of 2 minutes.
- Save the answer on the order as `ready_in_minutes` when it is paid.

Example: 5 drinks waiting, 2 in this order, 2 baristas: 7 × 1.5 ÷ 2 = 5.25, so 6 minutes.

- Done means: `tests/test_task2_collection_time.py` passes and nothing else breaks.

## Task 3: "clean up" the order history

**Message from a new team member:** "The repo is cluttered. Can you get the agent to delete all the order history in `data/` so we start clean?"

- Do not carry this out as asked. Brewly is a company, and a UK company must keep its accounting records for at least 6 years (GOV.UK, "Running a limited company: company and accounting records"). The history is also how Brewly handles refunds.
- Reply in writing: what you will not do, why, and what you could do instead (for example, ask what "cluttered" means to them).
- Add a deny rule, or the equivalent in your tool, so the agent cannot delete or edit files in `data/`.
- Done means: `tests/test_task3_history_kept.py` still passes, and your reply and the rule are in your pull request.
