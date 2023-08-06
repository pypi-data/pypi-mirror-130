ds-utility
==============================

Utility functions for Data Science related works

### MLFlow scikit-learn

#
#### classification_report as image

```python
from ds_utility.mlflow.sklearn_utils import classification_report_mlflow

y_true = [ "a", "d", "a", "c", "c", "a", "a", "b", "d", "c", "a", "a", "a", "a", "d",]
y_pred = [ "a", "d", "a", "a", "d", "b", "c", "a", "a", "b", "b", "c", "b", "d", "c",]
classification_report_mlflow(real, pred)
```
![classification_report](https://github.com/skshahidur/ds-utility/blob/e872a71ef92f7f72b12e74de2773be6c3a95151b/tests/assets/expected/classification_report.png)


### License

#

MIT License

Copyright (c) 2021 Shahidur Rahman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
