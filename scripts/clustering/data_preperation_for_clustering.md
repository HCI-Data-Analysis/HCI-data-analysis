# Data Preperation For Clustering

Containing methods `prepare_data_hci()` and `prepare_data_background()` that will take the impression survey result or cleaned background survey result and aggregate in a meaningful way that can be used for the clustering model. 

The average of student's response for each question category is obtained, negatively phrased questions are also made into consideration.

The resulting document will only contain the `id` column and a column for each question category.

For the impression survey the columns are:

- `id`
- `Confidence`
- `Gender`
- `Professional`
- `Identity`
- `Interest`

For the background survey the columns are:

- `id`
- `Extraversion`
- `Agreeableness`
- `Conscientiousness`	
- `Neuroticism`	
- `Openness`

Both dataset happens to have six columns, with five independent variables (dimensions) to perform clustering on.

    
