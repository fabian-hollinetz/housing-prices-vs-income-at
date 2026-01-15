# Housing Prices vs. Income in Austria

This repository contains a small, descriptive analysis comparing the development
of residential real estate prices with inflations-adjusted net incomes in Austria.

The goal is not to provide causal explanations or policy recommendations,
but to make long-term dynamics visible using publicly available data.

## Data Sources

- Real estate price snapshots based on Statistik Austria aggregates
- Inflations-adjusted net annual income indices (Statistik Austria)
  - 10% quantile
  - Median
  - 90% quantile
- Base year for comparison: 2015 = 100

## Methodology

- All series are indexed to 2015 = 100 to focus on relative development
- Income data is already inflation-adjusted
- No modeling or regression is applied
- Results are purely descriptive

## Result

![Housing vs Income](figures/housing_vs_income_index.png)

The shaded area shows the income distribution between the 10% and 90% quantile.
The solid income line represents the median.

## Notes

- Income data reflects net annual income of dependent employees
- Tax and transfer effects are included implicitly
- Real estate prices are aggregated across regions and categories

This analysis is intended as a starting point for discussion, not as a final statement.
