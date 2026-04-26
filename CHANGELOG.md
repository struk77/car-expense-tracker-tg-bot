# Changelog

## v1.1.0

### New features
- New `/income` command to record income entries (VAT refunds, sale proceeds, etc.). The latest odometer is recorded automatically.
- Purchase price now stores the original currency alongside the amount (e.g. `35000 EUR`). Existing car data is read via a fallback and will work without any migration; re-run `/setup` to store the new format.
- Stats: cost per km now shown in two lines — expenses only, and expenses including depreciation (linear 10%/year, zeroes at 10 years, minimum 1 year applied).
- Stats: all expense totals now include a last-30-days breakdown.
- Stats: removed the "total including purchase price" line.

### Bug fixes
- Category labels in expense confirmations and stats now respect the configured language (were hardcoded in Ukrainian).
- Fuel efficiency calculation no longer misorders rows with a missing odometer value.

### Migration from v1.0.0

The Google Sheets **Expenses** sheet has two renamed columns:

| Old name | New name |
|---|---|
| `pln_amount` | `base_amount` |
| `price_per_liter_pln` | `price_per_liter_base` |

Rename these two column headers manually in your spreadsheet before upgrading, otherwise `/stats` will show zero totals.
