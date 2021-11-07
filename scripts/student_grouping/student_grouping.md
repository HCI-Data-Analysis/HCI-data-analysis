# Student Grouping based on OCEAN values generated from their survey repsonses

## Running ANOVA

Before running ANOVA, we ran Levene's test to check whether the data had homogeneity of variance aka **
homoscedasticity**.

```python
from scipy.stats import levene

col = 'Final Score'
positive_group = overall_score_data[overall_score_data[facet_column_name] == 'Positive']
neutral_group = overall_score_data[overall_score_data[facet_column_name] == 'Neutral']
negative_group = overall_score_data[overall_score_data[facet_column_name] == 'Negative']
stat, p = levene(positive_group[col], neutral_group[col], negative_group[col])
print(stat, p)
1.3809137094974067
0.2544634295593595
```

Based on this result, the p value is greater than 0.05 which is our alpha value, so we fail to reject the null
hypothesis, which in this case is: "The data has homogenic variance".

So we can run ANOVA on this data.

```python
f_oneway(positive_group[col], neutral_group[col], negative_group[col])
F_onewayResult(statistic=0.060927202613047585, pvalue=0.9409145480545644)
```

So according to ANOVA, there isn't any statistically significant difference between final scores for students with
low/neutral/high openness

We ran the Levene test and ANOVA on the other OCEAN facets per activity type, and while most of them had very high p
values, there were two results in particular that were worth mentioning:

```
ANOVA Results for Pre/Post Tests Final Score with facet Neuroticism_group:
F_onewayResult(statistic=3.860654916843564, pvalue=0.023135267633160116)
```

