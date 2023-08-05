# Correlation Kit

A toolkit for estimating the correlation values between variables

## Installation
```pip
pip install correlation-kit
```

## Correlation between two continual variables
```python
import pandas as pd
from correlation_kit import CorrelationKit

# set a dataframe or read from a csv file
d = {'x': [1, 2, 3.5, 4], 'y': [3, 4, 4.5, 6]}
df = pd.DataFrame(data=d)

# set x label and y label for correlation
x = "x"
y = "y"

# calc
def get_correlation(x, y, corr_type):
    stat = 0
    p = 0
    if corr_type == "pearson":
        stat, p = CorrelationKit(df).get_pearson(x, y)
    elif corr_type == "spearman":
        stat, p = CorrelationKit(df).get_spearman(x, y)
    elif corr_type == "kendalltau":
        stat, p = CorrelationKit(df).get_kendalltau(x, y)
    return stat, p

# print results
print("pearson = ", get_correlation(x, y, "pearson"))
print("spearman = ", get_correlation(x, y, "spearman"))
print("kendalltau = ", get_correlation(x, y, "kendalltau"))
```

## Estimate correlation between binary and continual variables
```python
import pandas as pd
from correlation_kit import CorrelationKit

# set a dataframe or read from a csv file
d = {'x': ['large', 'large', 'small', 'small'], 'y': ['hot', 'hot', 'cold', 'cold'],'z':[0,1,2.5,3]}
df = pd.DataFrame(data=d)

# set x label and y label for correlation, which is suitable for binary variables
r_p,r_s,r_k=CorrelationKit(df).get_corr_between_category_and_continual('x','large','z') # large=1; otherewise 0

# results
print('pearson: ',r_p)
print('speraman: ',r_s)
print('kendalltau: ',r_k)

```

## Estimate F value between multiple-category variable and continual variables

```python
import pandas as pd
from correlation_kit import CorrelationKit

# set a dataframe or read from a csv file
d = {'x': ['large', 'large', 'middle','small', 'small'], 'y': ['hot', 'hot','warm', 'cold', 'cold'],'z':[0,1,2,2.5,3]}
df = pd.DataFrame(data=d)

# set x label and y label for correlation, which is suitable for multiple-category variables
F,p=CorrelationKit(df).get_f_oneway('x',['large','middle','small'],'z')

# results
print('F: ',F)
print('p: ',p)


```

## License
The `Correlation-Kit` project is provided by [Donghua Chen](https://github.com/dhchenx). 

