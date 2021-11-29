# Course Performance Analysis

### Requirements
 1. Key.csv (in keys folder)
 2. gradebook.csv (in same location as script)
 3. Quizzes submissions folder (in same location as script)
---

## Graphs
The first portion of the code generates graphs to allow us to analyze the course performance

## Final Score vs First Quiz Attempt Scores
The final portion of the code analyzes the final score vs the first quiz attempt scores. Initially a t-test was going
to be conducted, after analysis this led to a wilcoxon signed-rank test...

### Initial t-test exploration
    We will use a paired sample t test to determine if the averages between the two columns differ from each other
    because they are values from the same individuals of different conditions (first attempt tests vs last attempt)
    hypothesis: null hypothesis: the true mean difference is equal to zero therefore taking
                                 extra attempts has not increased the overall grade
                alternate hypothesis: the true mean difference is not equal to zero (two-tailed) therefore
                                      taking extra attempts has increased the overall grade

    We are setting our alpha level to be 0.05 or a 5% probability of rejecting the null hypothesis
    
    Shapiro-Wilks Test to determine normality (null hypothesis assumes that they are normally distributed)
    ShapiroResult(statistic=0.8274096250534058, pvalue=1.6519291360164723e-12)
    ShapiroResult(statistic=0.8776170015335083, pvalue=3.1659566634978376e-10)
        https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test
    The p-values are less than the specified alpha value, therefore we reject the null hypothesis and assume that
    they are not normally distributed. This means that we are not able to run a valid t-test on the data.
### Wilcoxon signed-rank test
    Therefore we can run a wilcoxon signed-rank test because it can handle non normal data
        https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test
        https://www.sciencedirect.com/topics/medicine-and-dentistry/wilcoxon-signed-ranks-test
    On a set of matched samples, it is a paired difference test like the paired Student's t-test (also known
    as the "t-test for matched pairs" or "t-test for dependent samples")
    For a paired sample test, the data consists of samples (X1 , Y1), … ,(Xn , Yn). 
    Each sample is a pair of measurements.
    We need to conclude that the first attempt only test score median, at a 0.05 significance, is different
    from the 93.0% median of the overall final score

    WilcoxonResult(statistic=19.0, pvalue=5.121623606912947e-28)
    The p-value is less than the specified alpha value, therefore we reject the null hypothesis and assume that there
    is a significant difference between the overall final score and the first atempt quiz final score.
