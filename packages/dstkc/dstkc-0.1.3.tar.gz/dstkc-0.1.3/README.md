# dstkc
data science toolkit and storage container

This toolkit is meant to be a storage container that organizes your data and data science
models so that it is easy to work with.  This class acts as both a pre-processor, as well
as a storage container

:param df: Pandas dataframe

:param model: data science model

:param y_col: column in df that contains dependent variable

:param x_cols: columns in df that contain independent variables

:param train_test_split_params: parameters for sci-kit learn's train test split function
    see https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    for reference

other attributes include:

:attr train_data - pandas dataframe with all training data

:attr test_data - pandas dataframe with all testing data


:attr x_data - pandas dataframe with all x data

:attr y_data - pandas dataframe with all y data


:attr x_test - pandas dataframe with all x testing data

:attr x_train - pandas dataframe with all x training data

:attr x_test_array - numpy array with all x testing data

:attr x_train_array - numpy array with all x training data


:attr y_test - pandas dataframe with all y testing data

:attr y_train - pandas dataframe with all y training data

:attr y_test_array - numpy array with all y testing data

:attr y_train_array - numpy array with all y training data

:attr model - store your model here for later use

:attr predictions - store your model's predictions here

:attr score - store a scoring or performance metric here

:attr notes - place for you to store any and all notes

:attr misc_container - dict style container for storing anything 
else you might need

here is an example of a few use cases

```
import pandas as pd
from operator import attrgetter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

from dstkc.tkc import DataScienceToolKit


def example_main():
    # here we read in the iris data set (because it's a classic)
    df = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
        names=[
             'sepal_length',
             'sepal_width',
             'petal_length',
             'petal_width',
             'species'
        ]
    )
    # we need to handle a bit of data pre processing,
    #     currently the toolkit doesn't handle for nulls or string->numeric
    df['species'] = df['species'].apply(
        lambda x: 0 if x == 'Iris-setosa' else 1 if x == 'Iris-versicolor' else 2
    )

    # there are two useful cases for this toolkit as it stands, one is cycling
    #     through columns if you're unsure what combination of columns to use
    all_x_cols = df.columns[:-1]
    y_col = df.columns[-1:]

    # here we are going to try different combinations of columns, and store
    #     the information. note how there is no mention of data processing
    #     other than our data cleaning with our dataframe
    toolkit_storage_container = []
    for i in range(1, len(all_x_cols)):
        # not technically useful in this instance, but naming
        #   the model will be something to revisit in the future
        model_name = 'knn'

        x_cols = all_x_cols[i:]

        # the class uses train test split from sklearn, the final argument are the
        #     parameters for the function call
        #     see: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
        #     for details
        dstk = DataScienceToolKit(
            df=df,
            model=KNeighborsClassifier(),
            y_col=y_col,
            x_cols=x_cols,
            train_test_split_params={
                'test_size': 0.3
            }
        )

        # each container can store notes, among other handy values, there is also
        #     a miscellaneous container which acts as a dictionary in case
        #     you want to have something else float around with all of your
        #     data and models
        dstk.notes = model_name

        # and just like that, you have all of your data ready to go, in one place!
        print(dstk.x_train)  # here is your data as a dataframe for inspection, debugging
        print(dstk.x_train_array)  # here is your dat as an array for your modeling

        print(dstk.y_train)  # here is your data as a dataframe for inspection, debugging
        print(dstk.y_train_array)  # here is your dat as an array for your modeling

        print(dstk.x_test)  # here is your data as a dataframe for inspection, debugging
        print(dstk.x_test_array)  # here is your dat as an array for your modeling

        print(dstk.y_test)  # here is your data as a dataframe for inspection, debugging
        print(dstk.y_test_array)  # here is your dat as an array for your modeling

        # please note that we fit and score the model using the model's native features
        #     so we can use any model, this is not only for scikit learn
        dstk.model.fit(dstk.x_train_array, dstk.y_train_array)

        # we can also store the predictions and score of the model, in any fashion or
        #   form you would like
        dstk.predictions = dstk.model.predict(dstk.x_test_array)
        dstk.score = dstk.model.score(
            dstk.x_test_array, dstk.y_test_array
        )

        # we're gonna store this for later, this is where the real use case comes in
        toolkit_storage_container.append(dstk)

    # now that we have finished iterating over a bunch of different column sets,
    #   maybe we want to know which had the best performance
    best_dstk = max(toolkit_storage_container, key=attrgetter('score'))

    # now we may want to know what the columns were, or inspect that
    #   dataset outside of our code
    print(best_dstk.x_cols)
    # best_dstk.train_data.to_csv('./train_data.csv')
    # best_dstk.test_data.to_csv('./test_data.csv')

    # most importantly, all of the data, along with the model, performance information,
    #     predictions, arrays, dataframes, and anything else are now sitting
    #     together, and you can use any feature of the model to inspect, or
    #     use any aspect of the work we have done, without
    #     altering any of your prior code

    # another use case is comparing model performance, not just column set performance
    #     (now names/notes become more important)

    model_dict = {
        'sgdc': SGDClassifier(),
        'gauss': GaussianNB(),
        'knn': KNeighborsClassifier(),
        'dtc': DecisionTreeClassifier(),
        'rfc': RandomForestClassifier(),
    }

    # re-initializing this for new example
    toolkit_storage_container = []

    for key_, value_ in model_dict.items():
        model_name = key_
        new_model = value_

        # note that in this instance, we are not declaring x cols, because we are going to
        #     use all columns other than the y_col, and that is default
        #     behaviour for the toolkit
        #     also, if the y col was in the first position of the dataframe,
        #     it would not have to be specified either

        dstk = DataScienceToolKit(
            df=df,
            model=new_model,
            y_col=y_col,
            train_test_split_params={
                'test_size': 0.3
            }
        )

        dstk.notes = model_name

        dstk.model.fit(
            dstk.x_train_array, dstk.y_train_array
        )
        dstk.predictions = dstk.model.predict(
            dstk.x_test_array
        )
        dstk.score = dstk.model.score(
            dstk.x_test_array, dstk.y_test_array
        )

        # here is an example of using the miscellaneous container to store a confusion matrix
        #     for later
        dstk.misc_container['confusion_matrix'] = confusion_matrix(
            dstk.y_test_array, dstk.predictions
        )

        toolkit_storage_container.append(dstk)

    # this time around, we want to know which model had the best score
    best_dstk = max(toolkit_storage_container, key=attrgetter('score'))

    # and yet again, we have all of the relevant information,
    #     like which model was best, what the performance was
    #     we also have all the models, in case we want to
    #     test or compare any aspect of them
    #     further more, one can combine the two cases
    #     and iterate over column sets, and model choices
    #     to quickly hone in on interesting data points,
    #     without having to clean the data or split the data
    #     and store the data in any way that usually causes
    #     (well at least for me) any headaches
    print(best_dstk.notes)
    print(best_dstk.score)
    print(best_dstk.misc_container['confusion_matrix'])

    print(
        '''
        hope you enjoy, and find this useful! 
        '''
    )


if __name__ == '__main__':
    example_main()
```
