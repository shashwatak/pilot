runner_config = {
    'iterations_per_run': 10000,
    'run_split': 0.6
}

logger_config = {
    'labels': ['phi'],
    'types':  ['float'],
    'keys':   {
        'state': ['phi'],
    }
}

predictor_config = {
    'serialization': {
        'path': '/tmp/pilot/default/satellite'
    }
}

world_config = {
    'dt': 5,
    'state': {
        'phi': 0.
    },
    'params': {},
}
