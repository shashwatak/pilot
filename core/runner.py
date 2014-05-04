class Runner:

    def __init__(self, config, world, predictor, guard=None, learning_enabled=False):
        self.config = config
        self.world = world
        self.predictor = predictor
        self.guard = guard
        self.learning_enabled = learning_enabled

        self.loggers = []

        self.i = 0
        self.run = 0
        self.disabled = False

    """ Public """

    def tick(self):
        if self.disabled:
            return

        self.i += 1
        state = self.world.observe()


        if not self.sanityCheck(state):
            self.world.terminate()
            self.disabled = True
            return

        prediction = self.runPredictor(state)

        self.world.tick()

        self.log(state, prediction)

    def sanityCheck(self, state):
        if not self.guard:
            return True

        return self.guard.check(state)

    def checkpointPredictor(self):
        if self.learning_enabled:
            print "Checkpointing predictor... DO NOT KILL DURING THIS TIME"
            self.predictor.checkpoint()

    def runPredictor(self, state):
        if self.learning_enabled:
            return self.predictor.learn(state)
        else:
            return self.predictor.predict(state)

    def newRun(self):
        self.run += 1
        print "Beginning a new run (" + str(self.run) + ")..."
        self.initPredictor()

    def midwayThroughRun(self):
        iterations_per_run = self.config['iterations_per_run']

        if not self.i or self.i % iterations_per_run == 0:
            return False

        split = self.config['run_split']
        current_i = self.i % iterations_per_run

        return (current_i % int(iterations_per_run * split) == 0)

    def addLogger(self, logger):
        self.loggers.append(logger)

    """ Private """

    def initPredictor(self):
        print "Initializing predictor..."
        state = self.world.observe()
        prediction = self.runPredictor(state)

    def resetPredictor(self):
        print "Resetting predictor..."
        self.predictor.resetState()

    def reset(self):
        print "Resetting..."
        self.world.resetState()
        self.resetPredictor()

    def log(self, state, prediction):
        for logger in self.loggers:
            logger.log(state, prediction)

    def shouldBeginNewRun(self, state):
        if self.i and (self.i % self.config['iterations_per_run'] == 0):
            return True

        return False
