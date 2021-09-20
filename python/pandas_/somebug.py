import numpy as np
import pandas as pd


def dummy_prep(data, method=None):
    varlist = data.columns[(data.dtypes == "category").values]
    if not method:
        return pd.get_dummies(data.loc[:, data.dtypes == "category"])
    if method == "drop_first":
        return pd.get_dummies(data.loc[:, data.dtypes == "category"], drop_first=True)
    if method == "deviation":
        dummies = pd.get_dummies(data.loc[:, data.dtypes == "category"])

        dummylist = {i: [x for x in dummies.columns if i in x] for i in varlist}
        for var in dummylist:
            if (dummies.values == 255).any():
                print(f"{var} before")
                import q

                q.d()
            dropout = dummylist[var][0]
            keepers = dummylist[var][1:]
            dummies.loc[dummies[dropout] == 1, keepers] = -1
            del dummies[dropout]
        if (dummies.values == 255).any():
            print(f"{var} after")
            import q

            q.d()

    return dummies


test1 = pd.DataFrame()
test1["cat2"] = pd.Categorical(np.random.randint(low=0, high=2, size=100))
test1["cat3"] = pd.Categorical(np.random.randint(low=0, high=3, size=100))
test1["cat4"] = pd.Categorical(np.random.randint(low=0, high=4, size=100))
print(test1.groupby("cat4").cat3.count())
print(test1.head())
dummy_prep(test1[["cat4", "cat3", "cat2"]], method="deviation").head()
