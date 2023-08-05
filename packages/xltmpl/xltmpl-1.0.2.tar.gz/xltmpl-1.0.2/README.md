## Install

```
pip install xltmpl==1.0.1
```

## Quick Start

```python
# -*- coding: utf-8 -*-
import pandas as pd
from xltmpl.xltmpl import XlTemplate

xlpath_tmpl = 'xlsx_template.xlsx' # xls format is allowed
xlpath_save = 'save.xlsx'

# place_holder is the value of all cells in the last row of the template sheet,
# that you can set the style and number format for each column.
with XlTemplate(tmpl_path=xlpath_tmpl, xlpath_save=xlpath_save, place_holder='{{}}') as tmpl:
    # append one row to Sheet1
    row = ['apple', 'orange', 'banana']
    tmpl.append_row('Sheet1', row)
    
    # append multi rows to the 1st sheet
    rows = [
        ['Jason', 'M', 23],
        ['Rose', 'F', 19]]
    tmpl.append_rows(1, rows)
    
    # append one row to the 2nd sheet, the first row is header, the second row is place_holder
    # Name      Age     Sex
    # {{}}      {{}}    {{}}
    record = {
        'Name': 'Micheal',
        'Age': 14,
        'Sex': 'M'
    }
    tmpl.append_dict(2, record, header_row=1, style_row=2)
    
    # append a dataframe to the 3rd sheet
    data = {
        'Name': ['Jason', 'Rose', 'Micheal'],
        'Age': [23, 19, 14],
    }
    df = pd.DataFrame(data)
    tmpl.append_dataframe(3, df)
```