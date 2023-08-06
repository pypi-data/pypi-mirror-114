"""
.. module:: d2m
   :synopsis: Dataframe health checker
.. moduleauthor:: Bonzoyang <github.com/bonzoyang>
"""

import pandas as pd

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
