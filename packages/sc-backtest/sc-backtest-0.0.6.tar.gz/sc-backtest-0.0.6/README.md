# Index Futures Simple Backtest Module (Personal Usage)

Chang Sun 
[Email](ynsfsc@126.com)

## Install and Update
```
pip install --upgrade sc-backtest
```

## Simple Test
* Check for factor validity
   * Statistical:
      * CDF
      * Markout
      * Hist
   * Time-Series:
      * Sign-Trade
      * Value-Trade
      * Threshold-Trade
   * Report
      * get_report

```
# x: factors
# y: asset's future ret

import pandas as pd
import numpy as np
from sc_backtest import simpletest

data = pd.read_csv('.\factor_and_ret.csv', index_col=0, header=0)
x = data.loc[:, 'factor']
y = data.loc[:, 'ret']
st = simpletest(is_day=True)
st.plot_cdf(x, y)
```

```
# x: factors
# y: asset's future ret

import pandas as pd
import numpy as np
import sc_backtest as sb

data = pd.read_csv('.\factor_and_ret.csv', index_col=0, header=0)
x = data.loc[:, 'factor']
y = data.loc[:, 'ret']
st = sb.simpletest(is_day=True)
data = st.simple_pnl(x, y, data_return=True)
report = sb.get_report(data['delta_med'], y)
```

## Technical Analysis
Variou moving average function
* SMA
* EMA
* WMA
* MMA
* QMA
* ...
```
import pandas as pd
import numpy as np
from sc_backtest import ta

wma = ta.wma(pd.Series(np.random.rand(100)), window=5)
```


## Example
Input your factor and uderlying asset's future return series with index type as DatetimeIndex and get the composite stat and time-series plots.
```
# x: factors
# y: asset's future ret

import pandas as pd
import numpy as np
from sc_backtest import simpletest

data = pd.read_csv('.\factor_and_ret.csv', index_col=0, header=0)
x = data.loc[:, 'factor']
y = data.loc[:, 'ret']
st = simpletest(is_day=True)
st.plot_composite(x, y, markout_periods=30, cdf_period2=5)
```
