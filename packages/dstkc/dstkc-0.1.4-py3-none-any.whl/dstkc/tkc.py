import sklearn.model_selection as skl_ms


class DataScienceToolKit:
    def __init__(self, df, model=None, y_col=None, x_cols=None, train_test_split_params={}):
        '''
        This toolkit is meant to be a storage container that organizes your data and data science
        models so that it is easy to work with.  This class acts as both a pre-processor, as well
        as a storage container
        :param df: Pandas dataframe for
        :param model: data science model
        :param y_col: column in df that contains dependent variable
        :param x_cols: columns in df that contain independent variables
        :param train_test_split_params: parameters for sci-kit learn's train test split function
            see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
            for reference
        '''
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
        self.misc_container = {}

    def split_x_y(self, df, y_col, x_cols):
        '''
        separates data into x data (independent variables) and
        y data (dependent variables).  Get's used at instantiation,
        can also be called outside of class as a stand alone function for
        quick and dirty use cases
        :param df: pandas dataframe
        :param y_col: column name with dependent variable
        :param x_cols: column names with independent variables
        :return: a series, and a data frame containing relevant data
        '''
        x = df.loc[:, x_cols]
        y = df[y_col]

        return x, y
