import sklearn.model_selection as skl_ms


class DataScienceToolKit:
    def __init__(self, df, model=None, y_col=None, x_cols=None, train_test_split_params={}):
        self.data = df
        if y_col is None:
            self.y_col = df.columns[0]
        else:
            self.y_col = y_col
        if x_cols is None:
            self.x_cols = [col for col in df.columns if col != self.y_col]
        else:
            self.x_cols = x_cols

        self.train_test_split_params = train_test_split_params

        self.train_data, self.test_data = skl_ms.train_test_split(
            df, **self.train_test_split_params
        )

        self.x_data, self.y_data = self.split_x_y(
            self.data,
            self.y_col,
            self.x_cols
        )

        self.x_train, self.y_train = self.split_x_y(
            self.train_data,
            self.y_col,
            self.x_cols
        )

        self.x_train_array = self.x_train.to_numpy()
        self.y_train_array = self.y_train.to_numpy()

        self.x_test, self.y_test = self.split_x_y(
            self.test_data,
            self.y_col,
            self.x_cols
        )

        self.x_test_array = self.x_test.to_numpy()
        self.y_test_array = self.y_test.to_numpy()

        self.model = model
        self.predictions = None
        self.score = None
        self.notes = None

    def split_x_y(self, df, y_col, x_cols):
        x = df.loc[:, x_cols]
        y = df[y_col]

        return x, y
