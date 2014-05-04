from core.predictor import Predictor
import satellite_model_params


class SatellitePhiPredictor(Predictor):

    def getModelParams(self):
        return satellite_model_params.MODEL_PARAMS

    def modelInputFromStateAndAction(self, state):
        return {
            'phi': state['phi']
        }
