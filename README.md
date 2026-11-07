# brewly-orders

Practice repository for Dhi's **Directing coding agents** unit (AI engineering path, Production stage).

Brewly is an invented UK coffee chain: 120 cafés, coffee at £3.50. Every number here is practice data.

This small Python service takes café orders: it prices the basket, charges the card through a pretend payment gateway, and keeps the order until the customer collects it. It has one bug, one missing feature and one request you should not carry out as asked. They are in [TASKS.md](TASKS.md).

## Start

1. Click **Use this template** on GitHub to make your own public copy, then clone it.
2. Use Python 3.10 or later. Install the test runner and run the tests:

   ```bash
   python -m pip install -r requirements.txt
   python -m pytest
   ```

3. Expect 9 failures on a fresh copy: the task 1 and task 2 tests fail until you finish those tasks. The task 3 tests pass now and must still pass at the end. The full run takes under 5 seconds on a laptop.

## How you are checked

- **GitHub Actions** runs the same tests on every pull request and every push to `main` (`.github/workflows/checks.yml`). A green tick on your pull request is your proof.
- **Your review.** Fill in [REVIEW.md](REVIEW.md) in your own words before you open the pull request.
- The tests are public, so an agent can read them. That is fine: the skill is directing the agent and checking its work, not hiding the answer.

## Rules

- Work on a branch and open a pull request. Never push straight to `main`.
- Never weaken, skip or delete a test to make it pass.
- No real card numbers, keys or customer data in this repository.

## Licence

MIT. Written by Dhi (dhiapp.co.uk) for learners.
