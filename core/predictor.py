import os
from nupic.frameworks.opf.modelfactory import ModelFactory


class Predictor:

    def __init__(self, config):
        self.model_params = self.getModelParams()
        self.is_learning_enabled = True
        self.last_prediction = None

        self.model_path = config['serialization']['path']

        self.initModel()

    """ To be overridden """

    def getModelParams(self):
        print "getModelParams needs to be overridden"

    def modelInputFromStateAndAction(self, state):
        return {}

    # Optional, only for predictors whose predicted field is a state field
    def stateFromPrediction(self, prediction, init_state):
        return {}

    """ Public """

    def learn(self, state):
        input = self.modelInputFromStateAndAction(state)
        result = self.model.run(input)
        prediction = self.predictionFromModelResult(result)
        self.last_prediction = prediction
        return prediction

    def predict(self, state):
        input = self.modelInputFromStateAndAction(state)

        self.disableLearning()
        result = self.model.run(input)
        self.enableLearning()

        prediction = self.predictionFromModelResult(result)
        self.last_prediction = prediction
        return prediction

    def imagine(self, state):

        def predict_closure(input_list):
            def predict(model_fork):
                model_fork.disableLearning()
                results = []
                for input in input_list:
                    result = model_fork.run(input)
                    results.append(result)
                return results
            return predict


        # apply the function for each action
        funcs = [predict_closure([self.modelInputFromStateAndAction(state)]) for action in action_list]
        results = self.imagination.imagine(funcs)
        predictions = [self.predictionFromModelResult(result[0]) for result in results]

        return predictions

    def enableLearning(self):
        self.is_learning_enabled = True
        self.model.enableLearning()

    def disableLearning(self):
        self.is_learning_enabled = False
        self.model.disableLearning()

    def resetState(self):
        self.model.resetSequenceStates()
        self.last_prediction = None

    def checkpoint(self):
        if self.is_learning_enabled:
            self.model.save(os.path.abspath(self.model_path))

    """ Helpers """

    def predictionSteps(self):
        return self.model_params['predictionSteps']

    def predictionFromModelResult(self, result):
        prediction = result.inferences['multiStepBestPredictions']
        return prediction

    """ Private """

    def initModel(self):
        if os.path.exists(os.path.abspath(self.model_path)):
            self.model = ModelFactory.loadFromCheckpoint(
                os.path.relpath(self.model_path))
        else:
            self.model = ModelFactory.create(self.model_params)

        predicted_field = self.model_params['predictedField']
        if predicted_field:
            self.model.enableInference({'predictedField': predicted_field})
