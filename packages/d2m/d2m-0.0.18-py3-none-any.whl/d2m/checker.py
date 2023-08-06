"""
.. module:: d2m
   :synopsis: Dataframe health checker
.. moduleauthor:: Bonzoyang <github.com/bonzoyang>
"""

import pandas as pd
import numpy as np

# data helth check
def duplicateCheck(dataframe, columnMask=None, axis = 0, returnWithoutTop=True):
    """This function checks duplicate row / col in a dataframe.

    :param pandas.DataFrame dataframe: The DataFrame being checked.
    :param list columnMask: Which columns are took off before duplicate checking.
    :param int axis: 0 for duplicate row check. 
                     1 for duplicate column check.
    :param bool returnWithoutTop: True will return 2 lists: "top" and  "last", which contains first duplicate and rest correspondingly; False will return all duplicates.
    :return: Either return "top" and "last" or return all duplicates, depending on "returnWithoutTop"
    :rtype: list

    Here's an example of usage for checker.duplicateCheck API:
    
    .. code-block:: python
        :linenos:
        
        from d2m.checker import duplicateCheck
        # List of Tuples
        employees = [('Mark', 37, 'Jacksonville', 'Male', 37, 'Male', 37),
                     ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                     ('Thomas ', 21, 'Omaha', 'Male', 21, 'Male', 21),
                     ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                     ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                     ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                     ('Thomas ', 36, 'Tampa', 'Male', 36, 'Male', 36),
                     ('Deborah', 39, 'Tucson', 'Female', 39, 'Female', 39),
                     ('Issac ', 21, 'Indianapolis', 'Male', 21, 'Male', 21)
                    ]

        # Creating a DataFrame object
        df = pd.DataFrame(employees,
                          columns = ['Name', 'Age','City', 'Gender', 'age', 'Sex', 'AGE'])

        duplicateCheck(df)
        # row [3, 4, 5] are duplicated with row [1]
        # return: [[1]], [[3, 4, 5]]
        
        duplicateCheck(df, columnMask=['Age','City', 'age', 'AGE'])
        # row [3, 4, 5] are duplicated with row [1]
        # row [6] are duplicated with row [2]
        # return: [[1], [2]], [[3, 4, 5], [6]]

        duplicateCheck(df, columnMask=['Name', 'Age', 'Gender', 'age', 'Sex', 'AGE'], 
                        returnWithoutTop=False)
        # row [3, 4, 5, 8] are duplicated with row [1]
        ## return: [[1, 3, 4, 5, 8]]
        
        duplicateCheck(df, axis=1)
        # column ['age', 'AGE'] are duplicated with column ['Age']
        # column ['Sex'] are duplicated with column ['Gender']
        # return: [['Age'], ['Gender']], [['age', 'AGE'], ['Sex']]
        
        duplicateCheck(df, columnMask=['City'], axis=1)
        # column ['age', 'AGE'] are duplicated with column ['Age']
        # column ['Sex'] are duplicated with column ['Gender']
        # return: [['Age'], ['Gender']], [['age', 'AGE'], ['Sex']]
        
        duplicateCheck(df, axis=1, returnWithoutTop=False)    
        # column ['age', 'AGE'] are duplicated with column ['Age']
        # column ['Sex'] are duplicated with column ['Gender']
        # return: [['Age', 'age', 'AGE'], ['Gender', 'Sex']]
    """

    df = dataframe
    if columnMask is None:
        columns = df.columns
    else:
        columns = df.columns.drop(columnMask)

    df = df[columns] if axis == 0 else df[columns].T
    columns = df.columns

    rc = 'row' if axis == 0 else 'column'
    

    index = df[df[columns].duplicated(keep=False)].index.tolist()
    df = df[columns].loc[index]
    unique = pd.unique(df.iloc[:,0]).tolist()

    if not index:
        print(f'no duplicated {rc}s are found')
        return None
    else:
        tops = []
        rests = []
        indices = []
        for u in unique:
            index = df[df.iloc[:,0]==u].index.tolist()
            indices += [index, ]
            tops +=[index[0:1],]
            rests += [index[1:], ]
            print(f'{rc} {rests[-1]} are duplicated with {rc} {tops[-1]}')
        if returnWithoutTop:
            return tops, rests
        else:
            return indices

def VCSummary(df, dvc=100, epsilon=0.05, delta=0.05, margin=0.05):
    """This function summarize various bound of number of samples under certain model complexity.

    :param pandas.DataFrame df: The DataFrame being checked.
    :param int dvc: VC dimension, which represents model complexity.
    :param float epsilon: The distance between in-sample error and out-of-sample error.
    :param float delta: Between (0, 1), probability of how possibly the model is learnable.
    :param float margin: Between (0, 1), extra percentage that your samples should exceed. 
    :return: Return a summary information of model
    :rtype: pandas.DataFrame

    Here's an example of usage for checker.VCSummary API:
    
    .. code-block:: python
        :linenos:
        
        from d2m.checker import VCSummary
        import numpy as np
        rng = np.random.default_rng(seed=42)
        
        #  Creating a DataFrame object
        df = pd.DataFrame(rng.random((1000, 25)))
        
        VCSummary(df, dvc=100, epsilon=0.05, delta=0.05)
        # return:
        # |                    number of |    type | log(bound) |  amount | model learnable |
        # |------------------------------|---------|------------|---------|-----------------|
        # |                 data samples |         |        NaN |    1000 |             NaN |
        # |             model parameters |         |        NaN |     100 |             NaN |
        # | experienced bound of samples |     exp | 330.392560 |     100 |           False |
        # |     general bound of samples | general | 318.205060 | 1000000 |           False |
        # |       loose bound of samples |   loose |  -1.300911 | 2127326 |           False |
        
        VCSummary(df, dvc=100, epsilon=0.05, delta=0.05, margin=0)
        # return:
        # |                    number of |    type | log(bound) |  amount | model learnable |
        # |------------------------------|---------|------------|---------|-----------------|
        # |                 data samples |         |        NaN |    1000 |             NaN |
        # |             model parameters |         |        NaN |     100 |             NaN |
        # | experienced bound of samples |     exp | 330.392560 |     100 |            True |
        # |     general bound of samples | general | 318.205060 | 1000000 |           False |
        # |       loose bound of samples |   loose |  -1.300911 | 2127326 |           False |        


        # Creating Another DataFrame object
        df = pd.DataFrame(rng.random((10000000, 10)))
        
        VCSummary(df, dvc=1000, epsilon=0.1, delta=0.1, margin=0)
        # return:
        # |                    number of |    type |   log(bound) |   amount | model learnable |
        # |------------------------------|---------|--------------|----------|-----------------|
        # |                 data samples |         |          NaN | 10000000 |             NaN |
        # |             model parameters |         |          NaN |     1000 |             NaN |
        # | experienced bound of samples |     exp |  4289.132056 |    10000 |            True |
        # |     general bound of samples | general | -5198.367944 | 10000000 |            True |
        # |       loose bound of samples |   loose |    -0.999690 |  5643334 |            True |

    """    
    def log10Bound(N, dvc, epsilon):
        return np.log10(4)+dvc*(np.log10(2)+np.log10(N))-(0.125*N*epsilon**2)
    
    def rootLocationSolver(dvc, epsilon, delta):
        # phase 1: locate the power of 2
        N = 1
        while log10Bound(N, dvc, epsilon) > delta:
            N = N*2

        # phase 2: root locate to digits
        l = N//2
        r = N
        m = (l+r)//2
        trial = 1000
        while (abs(log10Bound(m, dvc, epsilon) - np.log10(delta)) > 1e-6) and abs(l-r) > 1 :
            if log10Bound(m, dvc, epsilon) - np.log10(delta) > 0:
                l = m
                m = (l+r)//2
            else:
                r = m
                m = (l+r)//2

            trial -= 1
            if trial < 0:
                break
        else:
            N=m
        
        return N
    
    samples, n1, n2, n3 = df.shape[0], 10*dvc, 10000*dvc, rootLocationSolver(dvc, epsilon, delta)
    margin = 1 + margin
    summary = pd.DataFrame({'number of':['data samples', 'model parameters', 'experienced bound of samples', 'general bound of samples', 'loose bound of samples'],
                            'type':['', '', 'exp', 'general', 'loose'],
                            'log(bound)':[np.nan, np.nan, log10Bound(n1, dvc, epsilon), log10Bound(n2, dvc, epsilon), log10Bound(n3, dvc, epsilon)],
                            'amount':[samples, dvc, n1, n2, n3],
                            f'model learnable':[np.nan, np.nan, samples >= n1*margin, samples >= n2*margin, samples >= n3*margin]})

    return summary
    
def VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='exp'):
    """This function returns number of samples under certain model complexity.

    :param pandas.DataFrame df: The DataFrame being checked.
    :param int dvc: VC dimension, which represents model complexity.
    :param float epsilon: The distance between in-sample error and out-of-sample error.
    :param float delta: Between (0, 1), probability of how possibly the model is learnable.
    :return: The amount than your samples should exceed.
    :rtype: int

    Here's an example of usage for checker.VCCheck API:
    
    .. code-block:: python
        :linenos:
        
        from d2m.checker import VCCheck
        import numpy as np
        rng = np.random.default_rng(seed=42)
        
        #  Creating a DataFrame object
        df = pd.DataFrame(rng.random((1000, 25)))
        print(VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='exp'),
              VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='general'),
              VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='loose'))
        # 1000 1000000 2127326
        
        
        # Creating Another DataFrame object
        df = pd.DataFrame(rng.random((10000000, 10)))
        print(VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='exp'),
              VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='general'),
              VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='loose'))  
        # 10000 10000000 5643334
    """
    summary = VCSummary(df, dvc, epsilon, delta)
    return summary[summary.type==type].amount.values[0]


if __name__ == '__main__':
    # List of Tuples
    employees = [('Mark', 37, 'Jacksonville', 'Male', 37, 'Male', 37),
                 ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                 ('Thomas ', 21, 'Omaha', 'Male', 21, 'Male', 21),
                 ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                 ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                 ('Ruth', 29, 'Indianapolis', 'Female', 29, 'Female', 29),
                 ('Thomas ', 36, 'Tampa', 'Male', 36, 'Male', 36),
                 ('Deborah', 39, 'Tucson', 'Female', 39, 'Female', 39),
                 ('Issac ', 21, 'Indianapolis', 'Male', 21, 'Male', 21)
                ]

    # Creating a DataFrame object
    df = pd.DataFrame(employees,
                      columns = ['Name', 'Age','City', 'Gender', 'age', 'Sex', 'AGE'])   
    
    duplicateCheck(df)
    # row [3, 4, 5] are duplicated with row [1]
    # return: [[1]], [[3, 4, 5]]
    
    duplicateCheck(df, columnMask=['Age','City', 'age', 'AGE'])
    # row [3, 4, 5] are duplicated with row [1]
    # row [6] are duplicated with row [2]
    # return: [[1], [2]], [[3, 4, 5], [6]]
    
    duplicateCheck(df, columnMask=['Name', 'Age', 'Gender', 'age', 'Sex', 'AGE'], 
                    returnWithoutTop=False)
    # row [3, 4, 5, 8] are duplicated with row [1]
    # return: [[1, 3, 4, 5, 8]]
    
    duplicateCheck(df, axis=1)
    # column ['age', 'AGE'] are duplicated with column ['Age']
    # column ['Sex'] are duplicated with column ['Gender']
    # return: [['Age'], ['Gender']], [['age', 'AGE'], ['Sex']]
    
    duplicateCheck(df, columnMask=['City'], axis=1)
    # column ['age', 'AGE'] are duplicated with column ['Age']
    # column ['Sex'] are duplicated with column ['Gender']
    # return: [['Age'], ['Gender']], [['age', 'AGE'], ['Sex']]
    
    duplicateCheck(df, axis=1, returnWithoutTop=False)    
    # column ['age', 'AGE'] are duplicated with column ['Age']
    # column ['Sex'] are duplicated with column ['Gender']
    # return: [['Age', 'age', 'AGE'], ['Gender', 'Sex']]


if __name__ == '__main__':
    import numpy as np
    rng = np.random.default_rng(seed=42)
    
    #  Creating a DataFrame object
    df = pd.DataFrame(rng.random((1000, 25)))
    
    VCSummary(df, dvc=100, epsilon=0.05, delta=0.05)
    # return:
    # |                    number of |    type | log(bound) |  amount | model learnable |
    # |------------------------------|---------|------------|---------|-----------------|
    # |                 data samples |         |        NaN |    1000 |             NaN |
    # |             model parameters |         |        NaN |     100 |             NaN |
    # | experienced bound of samples |     exp | 330.392560 |     100 |           False |
    # |     general bound of samples | general | 318.205060 | 1000000 |           False |
    # |       loose bound of samples |   loose |  -1.300911 | 2127326 |           False |
    
    VCSummary(df, dvc=100, epsilon=0.05, delta=0.05, margin=0)
    # return:
    # |                    number of |    type | log(bound) |  amount | model learnable |
    # |------------------------------|---------|------------|---------|-----------------|
    # |                 data samples |         |        NaN |    1000 |             NaN |
    # |             model parameters |         |        NaN |     100 |             NaN |
    # | experienced bound of samples |     exp | 330.392560 |     100 |            True |
    # |     general bound of samples | general | 318.205060 | 1000000 |           False |
    # |       loose bound of samples |   loose |  -1.300911 | 2127326 |           False |        
    
    
    # Creating Another DataFrame object
    df = pd.DataFrame(rng.random((10000000, 10)))
    
    VCSummary(df, dvc=1000, epsilon=0.1, delta=0.1, margin=0)
    # return:
    # |                    number of |    type |   log(bound) |   amount | model learnable |
    # |------------------------------|---------|--------------|----------|-----------------|
    # |                 data samples |         |          NaN | 10000000 |             NaN |
    # |             model parameters |         |          NaN |     1000 |             NaN |
    # | experienced bound of samples |     exp |  4289.132056 |    10000 |            True |
    # |     general bound of samples | general | -5198.367944 | 10000000 |            True |
    # |       loose bound of samples |   loose |    -0.999690 |  5643334 |            True |


if __name__ == '__main__':
        import numpy as np
        rng = np.random.default_rng(seed=42)
        
        #  Creating a DataFrame object
        df = pd.DataFrame(rng.random((1000, 25)))
        print(VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='exp'),
              VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='general'),
              VCCheck(df, dvc=100, epsilon=0.05, delta=0.05, type='loose'))
        # 1000 1000000 2127326
        
        
        # Creating Another DataFrame object
        df = pd.DataFrame(rng.random((10000000, 10)))
        print(VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='exp'),
              VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='general'),
              VCCheck(df, dvc=1000, epsilon=0.1, delta=0.1, type='loose'))  
        # 10000 10000000 5643334
