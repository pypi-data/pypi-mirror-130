import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold



class DS:
    """
    /**
    When creating an instance, the following parameters are attributed.

    data: Overall data
    predictor_names : List of names of predictor features
    target_name: name of the target column
    scalers : A list of various scaler
    encoders : Dictionary, key is encoded feature name, value is encoders
    fill_nan : Dictionary, The key is "replace" ans "fill_nan".
               The value for each key can also dictionary and fill values for each column.
    outliers : Dictionary, the key is categorical or nubmerical, the value is upper, lower bound.
    "categorical"'s value is dictionary, "numerical"'s value is also dictionary,
                                                        and key is feature name, value is list of upper,lower bound.

    models : A list of various models.
    params : A list of model hyper paremeters.
    k_fold : A list of k values.

    **/
    """

    def __init__(self, data, predictor_names, target_name, test_size, scalers=None, encoders=None, fill_nan=None,
                 outliers=None, models=None, params=None, k_fold=None):
        self.data = data
        self.predictor_names = predictor_names
        self.target_name = target_name
        self.test_size = test_size
        self.scalers = scalers
        self.encoders = encoders
        self.fill_nan = fill_nan
        self.outliers = outliers
        self.models = models
        self.params = params
        self.k_fold = k_fold

    def run(self, random):
        self.preprocessing()
        self.build_test_models(random)
        self.find_best()

    def preprocessing(self):

        # handling missing values
        if self.fill_nan != None:
            if "replace" in self.fill_nan:
                self.data.replace(self.fill_nan["replace"], inplace=True)
            if "fill_nan" in self.fill_nan:
                for key, value in self.fill_nan["fill_nan"].items():
                    if value == "mean":
                        self.data[key] = self.data[key].apply(pd.to_numeric)
                        self.data[key].fillna(self.data[key].mean(), inplace=True)
                    elif value == "max":
                        self.data[key] = self.data[key].apply(pd.to_numeric)
                        self.data[key].fillna(self.data[key].max(), inplace=True)
                    elif value == "min":
                        self.data[key] = self.data[key].apply(pd.to_numeric)
                        self.data[key].fillna(self.data[key].min(), inplace=True)
                    else:
                        self.data[key].fillna(value, inplace=True)

        # handling outliers
        if self.outliers != None:
            if "categorical" in self.outliers:
                for key, value in self.outliers["categorical"].items():
                    for outlier in value:
                        self.data.drop(self.data[self.data[key] == outlier].index, inplace=True)

            if "numerical" in self.outliers:
                for key, value in self.outliers["numerical"].items():
                    self.data.drop(self.data[self.data[key] > value[0]].index, inplace=True)
                    self.data.drop(self.data[self.data[key] < value[1]].index, inplace=True)

        # encoding categorical values
        if self.encoders != None:
            for name, encoder in self.encoders.items():
                encoded_data = encoder.fit_transform(self.data[name].values.reshape(-1, 1)).toarray()
                encoded_data = pd.DataFrame(encoded_data)
                self.data.drop(columns=name, inplace=True)
                self.data = pd.concat([encoded_data, self.data], axis=1)
                self.predictor_names = self.data.columns[:-1]

        self.predictor = self.data[self.predictor_names]
        self.target = self.data[self.target_name]

        # scaling
        if self.scalers != None:
            self.scaled_data = []
            for scaler in self.scalers:
                self.scaled_data.append(pd.DataFrame(scaler.fit_transform(
                    self.predictor), columns=self.predictor.columns))

    def build_test_models(self, random):
        self.grid = []
        for fold in self.k_fold:
            kf = KFold(n_splits=fold, shuffle=True, random_state=random)
            for i in range(len(self.models)):
                grid = GridSearchCV(self.models[i], param_grid=self.params[i],
                                    cv=kf,
                                    n_jobs=-1,
                                    verbose=2)
                if self.scalers != None:
                    for s_data in self.scaled_data:
                        X_train, X_test, y_train, y_test = train_test_split(s_data, self.target,
                                                                            random_state=random,
                                                                            test_size=self.test_size)
                        grid.fit(X_train, y_train)
                        grid.score(X_test, y_test)
                        self.grid.append(grid)

    def find_best(self):
        best_score = 0
        for grid in self.grid:
            if grid.best_score_ >= best_score:
                best_score = grid.best_score_
                best_parameter = grid.best_params_
        self.best_score = best_score
        self.best_params = best_parameter

