import pandas as pd
import numpy as np
from itertools import islice

import umap
from sklearn.experimental import enable_halving_search_cv
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV,\
    HalvingGridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.svm import SVC

import helpers


class SUMAP:
    def __init__(self,
                 freq_thres=0.3,
                 log=True,
                 gridsearch='half',
                 n_neighbors=list(range(5, 40, 5)),
                 min_dist=[0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5],
                 n_components=3,
                 cv=5,
                 min_resources='smallest',
                 factor=3,
                 score_func=metrics.f1_score,
                 average='weighted',
                 random_state=None,
                 ):
        """Define a UMAP-SVM pipeline with tunable UMAP parameters
        ----
        params for gridsearch:
        n_neighbors: -> list, number of neighbors in UMAP
        min_dist: -> list, minimum distance in UMAP

        other params:
        n_components: ->int, no. of dimension UMAP returns, usually 2 or 3
        cv: -> int (if not oversampled), otherwise self.cv (not need to define)
            default is stratified Kfold
            Notice: it defines the inner loop if it is a nested CV
        scorer -> metrics.scorer
        ----
        """

        freq_thres = helpers.FREQ_THRES(freq_thres=freq_thres)

        log = helpers.LOG(log=log)

        svc = SVC(random_state=random_state)

        mapper = umap.UMAP(random_state=random_state,
                           n_components=n_components)

        scorer = metrics.make_scorer(score_func=score_func,
                                     average=average,
                                     )

        pipeline = Pipeline([('freq', freq_thres),
                             ('log', log),
                             ('umap', mapper),
                             ('svc', svc),
                             ])

        params_grid_pipeline = {
            'umap__n_neighbors': n_neighbors,
            'umap__min_dist': min_dist,
            }

        if gridsearch == 'full':
            self.clf_pipeline = GridSearchCV(pipeline,
                                             params_grid_pipeline,
                                             cv=cv,
                                             scoring=scorer,
                                             n_jobs=-1,  # use all processors
                                             )
        elif gridsearch == 'half':
            self.clf_pipeline = \
                HalvingGridSearchCV(pipeline,
                                    params_grid_pipeline,
                                    cv=cv,
                                    scoring=scorer,
                                    n_jobs=-1,
                                    min_resources=min_resources,
                                    factor=factor,
                                    random_state=random_state
                                    )

    def _load_data(self, X, y):
        """load X and y"""
        self.Xtrain = X

        # y if categories, needs to be transformed to number before fit
        self.le = LabelEncoder()
        self.ytrain = self.le.fit_transform(y)

    def fit(self,
            X,
            y):
        """Fit a get_pipeline() object with Xtrain and ytrain
        Frequency threshold of Xtrain if needed freq_thres True
        """

        self._load_data(X, y)

        self.clf_pipeline.fit(self.Xtrain, self.ytrain)

        return self

    def transform(self,
                  X=None):

        pipeline_transform = self.clf_pipeline.best_estimator_[:-1]

        if X is None:
            Xtransform_ = pipeline_transform.transform(self.Xtrain)
        else:
            Xtransform_ = pipeline_transform.transform(X)

        return Xtransform_

    def _predict(self,
                 X=None):
        if X is None:
            ypred = self.clf_pipeline.predict(self.Xtrain)
        else:
            ypred = self.clf_pipeline.predict(X)

        return ypred

    def predict(self,
                X=None):

        ypred = self._predict(X)

        return self.le.inverse_transform(ypred)

    def score(self,
              X=None,
              y=None):
        """Return score depends on scorer used
        """
        if X is None and y is None:
            X = self.Xtrain
            y = self.ytrain
        elif X is not None and y is not None:
            if isinstance(y, pd.Series):
                y = self.le.transform(y)
        else:
            raise ValueError

        return self.clf_pipeline.score(X, y)

    def plot_cmatrix(self,
                     X=None,
                     y=None,
                     ):

        if X is None and y is None:
            y = self.ytrain
        elif X is not None and y is not None:
            if isinstance(y, pd.Series):
                y = self.le.transform(y)
        else:
            raise ValueError

        ypred = self._predict(X)

        return helpers.plot_cmatrix(y,
                                    ypred,
                                    cmapper=self.le,
                                    )

    def plot_embeddings(self,
                        X=None,
                        y=None,
                        elev=30,
                        azim=30,
                        ):
        """return scatter plots of embeddings and labels
        When X and y not given, use the training data
        """

        # get embeddings from the fitted pipeline
        Xtransform_ = self.transform(X)

        if X is None and y is None:
            cmapper_ = self.le
            y = self.ytrain
        elif X is not None and y is not None:
            cmapper_ = self.le
            if isinstance(y, pd.Series):
                cmapper_ = LabelEncoder()
                y = cmapper_.fit_transform(y)
        else:
            raise ValueError

        # plot 2d if Xtransform has 2 columns
        if Xtransform_.shape[1] == 2:
            return helpers.plot_bar(Xtransform_,
                                    y,
                                    cmapper=cmapper_,
                                    title='N = {n}'.format(n=len(y)),
                                    )

        # plot 3d if Xtransform has 3 columns
        elif Xtransform_.shape[1] == 3:
            return helpers.plot_bar3d(Xtransform_,
                                      y,
                                      cmapper=cmapper_,
                                      title='N = {n}'.format(n=len(y)),
                                      elev=elev,
                                      azim=azim,
                                      )


class SUMAP_nestedCV(SUMAP):

    def __init__(self,
                 n_splits_outer=5,
                 freq_thres=0.3,
                 log=True,
                 gridsearch='half',
                 n_neighbors=list(range(5, 40, 5)),
                 min_dist=[0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5],
                 n_components=3,
                 cv=5,
                 min_resources='smallest',
                 factor=3,
                 score_func=metrics.f1_score,
                 average='weighted',
                 random_state=None,
                 ):

        self.outer_cv = \
            StratifiedKFold(n_splits=n_splits_outer,
                            shuffle=True,  # each fold is independent
                            random_state=random_state)

        super().__init__(freq_thres,
                         log,
                         gridsearch,
                         n_neighbors,
                         min_dist,
                         n_components,
                         cv,
                         min_resources,
                         factor,
                         score_func,
                         average,
                         random_state,
                         )

    def fit(self,
            X,
            y,
            n_splits_outer=5,
            estimator=None,):
        """nested CV
        Samples were split to train and test
        Model is developed in train
        Model scores in test
        since all outer_cv.split are technically the same,
        the train test was taken from the final split as default

        Parameters
        ----------
        - n_splits_outer: int, no. of folds of outer CV
        - estimator: string, specify the model to return
            If 'best' return the one with highest test score
            If 'random' return a randomly chosen model from outer CV
            If 'average' return the one with median performace
            else return the last one (default)
        """

        self._load_data(X, y)

        self.outer_cvscores = []
        outer_pipelines = []

        n_outer = 0
        for train_id, test_id in self.outer_cv.split(self.Xtrain, self.ytrain):
            Xtrain, Xtest = \
                self.Xtrain.iloc[train_id], self.Xtrain.iloc[test_id]
            ytrain, ytest = self.ytrain[train_id], self.ytrain[test_id]

            self.clf_pipeline.fit(Xtrain, ytrain)

            outer_pipelines.append(self.clf_pipeline)

            # measure the model performance (chosen by inner cv) on outer cv
            Xtest_score = self.clf_pipeline.score(Xtest, ytest)

            self.outer_cvscores.append(Xtest_score)

            print('n_outer =', n_outer)
            # print ('Xtrain.shape', Xtrain.shape)
            # print ('Xtest.shape', Xtest.shape)
            # print ('ytrain.shape', ytrain.shape)
            # print ('ytest.shape', ytest.shape)
            print(Xtest_score)

            n_outer += 1

        print('Scores of {n} models: {mean} +/- {std}'
              .format(n=n_splits_outer,
                      mean=np.mean(self.outer_cvscores),
                      std=np.std(self.outer_cvscores)
                      )
              )

        if estimator == 'best':
            chosen_split = np.argmax(self.outer_cvscores)

        elif estimator == 'random':
            chosen_split = np.random.choice(n_splits_outer)

        elif estimator == 'average':
            chosen_split = helpers.argmedian(self.outer_cvscores)

        try:
            train_id, test_id = next(islice(self.outer_cv.split(X, y),
                                            chosen_split,
                                            chosen_split + 1
                                            )
                                     )
            self.Xtest, self.ytest = \
                self.Xtrain.iloc[test_id], self.ytrain[test_id]

            self.Xtrain, self.ytrain = \
                self.Xtrain.iloc[train_id], self.ytrain[train_id]

            self.clf_pipeline = outer_pipelines[chosen_split]

        except NameError:
            self.Xtrain, self.ytrain = Xtrain, ytrain
            self.Xtest, self.ytest = Xtest, ytest

        return self
