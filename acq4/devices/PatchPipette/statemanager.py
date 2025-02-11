import queue
import sys
from collections import OrderedDict
from typing import Optional

from acq4 import getManager
from acq4.util import Qt
from acq4.util.debug import printExc
from pyqtgraph import disconnect
from . import states


class PatchPipetteStateManager(Qt.QObject):
    """Used to handle state transitions and to spawn background threads for pipette automation

    State manager affects:
     - pipette state ('bath', 'seal', 'whole cell', etc.)
     - clamp mode
     - clamp holding value
     - pressure
     - test pulse
     - pipette position

    Note: all the real work is done in the individual state classes (see acq4.devices.PatchPipette.states)
    """

    stateHandlers = OrderedDict(
        [
            (state.stateName, state)
            for state in [
                states.OutState,
                states.BathState,
                states.ApproachState,
                states.CellDetectState,
                states.SealState,
                states.CellAttachedState,
                states.BreakInState,
                states.WholeCellState,
                states.ResealState,
                states.BlowoutState,
                states.BrokenState,
                states.FouledState,
                states.CleanState,
                states.NucleusCollectState,
                states.MoveNucleusToHomeState,
            ]
        ]
    )

    sigStateChanged = Qt.Signal(object, object)  # self, PatchPipetteState
    _sigStateChangeRequested = Qt.Signal(object, object, bool)  # state, return queue, managerHandlesErrors
    sigProfileChanged = Qt.Signal(object, object)  # self, profile_name

    profiles: dict[str: dict[str: dict[str: object]]] = {}  # {profile_name: {state_name: {config_options}}}
    _profilesLoadedFromConfig = False

    def __init__(self, dev):
        Qt.QObject.__init__(self)
        self.dev = dev
        self.dev.sigStateChanged.connect(self.stateChanged)
        self.dev.sigActiveChanged.connect(self.activeChanged)
        self.currentJob = None
        self._profile = None
        self._managerHandlesErrors = True

        self._sigStateChangeRequested.connect(self._stateChangeRequested)

        if 'default' in self.listProfiles():
            self.setProfile('default')

    @classmethod
    def listProfiles(cls):
        cls._loadGlobalProfilesOnce()
        return list(cls.profiles.keys())

    @classmethod
    def listStates(cls):
        return list(cls.stateHandlers.keys())

    @classmethod
    def getStateClass(cls, name) -> states.PatchPipetteState:
        return cls.stateHandlers[name]

    @classmethod
    def getProfileConfig(cls, name):
        cls._loadGlobalProfilesOnce()
        if name not in cls.profiles:
            raise KeyError(f"Unknown patch profile {name}")
        return cls.profiles[name]

    @staticmethod
    def _loadGlobalProfilesOnce():
        if PatchPipetteStateManager._profilesLoadedFromConfig:
            return
        PatchPipetteStateManager._profilesLoadedFromConfig = True
        man = getManager()
        for k, v in man.config.get('misc', {}).get('patchProfiles', {}).items():
            v = v.copy()
            PatchPipetteStateManager.addProfile(name=k, config=v)

    @classmethod
    def addProfile(cls, name: str, config: dict, overwrite=False):
        assert overwrite or name not in cls.profiles, f"Patch profile {name} already exists"
        mistakes = []
        for state, state_config in config.items():
            if state == 'copyFrom':
                if not isinstance(state_config, str):
                    mistakes.append(f"Invalid copyFrom value {state_config!r} in profile {name}")
                if state_config not in cls.profiles:
                    mistakes.append(f"Unknown profile {state_config!r} to copy from in profile {name}")
                continue
            if state not in cls.stateHandlers:
                mistakes.append(f"Unknown patch state {state!r} in profile {name}")
                continue
            if not isinstance(state_config, dict):
                mistakes.append(f"Invalid configuration for state {state!r} in profile {name}")
                continue
            for param, value in state_config.items():
                if not isinstance(param, str):
                    mistakes.append(f"Invalid parameter name {param!r} in state {state!r} of profile {name}")
                    continue
                if param not in cls.getStateClass(state).defaultConfig():
                    mistakes.append(f"Unknown parameter {param!r} in state {state!r} of profile {name}")
        if mistakes:
            raise ValueError(f"Errors in profile {name}:\n" + "\n".join(mistakes))
        cls.profiles[name] = config

    @classmethod
    def getStateConfig(cls, state: str, profile: Optional[str]):
        """
        Return the configuration options for the given state and profile, or just the defaults if no profile is
        specified.
        """
        if profile is None:
            config = {}
        else:
            config = cls.getProfileConfig(profile)
        if copy_from := config.get('copyFrom', None):
            defaults = cls.getStateConfig(state, copy_from)
        else:
            defaults = cls.getStateClass(state).defaultConfig()
        config = config.get(state, {})
        return {
            param: config.get(param, defaults.get(param, None))
            for param in set(list(defaults.keys()) + list(config.keys()))
        }

    def setProfile(self, profile: str):
        """Set the current patch profile."""
        self._profile = profile
        self.sigProfileChanged.emit(self, profile)

    def getState(self):
        """Return the currently active state.
        """
        return self.currentJob

    def stateChanged(self, oldState, newState):
        """Called when state has changed (possibly by user)
        """
        pass

    def requestStateChange(self, state, managerHandlesErrors):
        """Pipette has requested a state change; either accept and configure the new
        state or reject the new state.

        Return the name of the state that has been chosen.
        """
        # state changes involve the construction of numerous QObjects with signal/slot connections;
        # the individual state classes assume that they are owned by a thread with an event loop.
        # SO: we need to process state transitions in the main thread. If this method is called
        # from the main thread, then the emit() below will be processed immediately. Otherwise,
        # we wait until the main thread processes the signal and sends back the result.
        returnQueue = queue.Queue()
        self._sigStateChangeRequested.emit(state, returnQueue, managerHandlesErrors)
        try:
            success, ret = returnQueue.get(timeout=10)
        except queue.Empty as e:
            raise TimeoutError("State change request timed out.") from e

        if success:
            return ret
        sys.excepthook(*ret)
        raise RuntimeError(f"Error requesting state change to {state!r}; original exception appears above.")

    def _stateChangeRequested(self, state, returnQueue, managerHandlesErrors):
        try:
            if state not in self.stateHandlers:
                raise ValueError(f"Unknown patch pipette state {state!r}")
            ret = (True, self.configureState(state, managerHandlesErrors))
        except Exception as exc:
            ret = (False, sys.exc_info())
        returnQueue.put(ret)

    def configureState(self, state, managerHandlesErrors, *args, **kwds):
        oldJob = self.currentJob
        allowReset = kwds.pop('_allowReset', True)
        self.stopJob(allowNextState=False)
        try:
            self._managerHandlesErrors = managerHandlesErrors
            stateHandler = self.stateHandlers[state]

            # assemble state config from defaults and anything specified in args here
            config = self.getStateConfig(state, self._profile)
            config.update(kwds.pop('config', {}))
            kwds['config'] = config

            job = stateHandler(self.dev, *args, **kwds)
            job.sigStateChanged.connect(self.jobStateChanged)
            job.sigFinished.connect(self.jobFinished)
            oldState = None if oldJob is None else oldJob.stateName
            self.currentJob = job
            self.dev._setState(state, oldState)  # logging / accounting
            job.initialize()
            self.sigStateChanged.emit(self, job)
            return job
        except Exception:
            # in case of failure, attempt to restore previous state
            self.currentJob = None
            if not allowReset or oldJob is None:
                raise
            try:
                self.configureState(oldJob.stateName, managerHandlesErrors, _allowReset=False)
            except Exception:
                printExc("Error occurred while trying to reset state from a previous error:")
            raise

    def activeChanged(self, pip, active):
        if active and self.getState() is not None:
            self.configureState(self.getState().stateName, managerHandlesErrors=False)
        else:
            self.stopJob()
            if self.dev.clampDevice is not None:
                self.dev.clampDevice.enableTestPulse(False)
            if self.dev.pressureDevice is not None:
                self.dev.pressureDevice.setPressure(source='atmosphere')

    def quit(self):
        disconnect(self.dev.sigStateChanged, self.stateChanged)
        disconnect(self.dev.sigActiveChanged, self.activeChanged)
        self.stopJob(allowNextState=False)

    def stopJob(self, allowNextState=True):
        job = self.currentJob
        if job is not None:
            # disconnect; we'll call jobFinished directly
            disconnect(job.sigFinished, self.jobFinished)
            job.stop()
            try:
                job.wait(timeout=10)
            except job.Timeout:
                printExc(f"Timed out waiting for job {job} to complete")
            except Exception:
                if self._managerHandlesErrors:
                    printExc(f"{self.dev.name()} failed in state {job.stateName}:")
            self.jobFinished(job, allowNextState=allowNextState)

    def jobStateChanged(self, job, state):
        self.dev.emitNewEvent("state_event", {'state': job.stateName, 'info': state})

    def jobFinished(self, job, allowNextState=True):
        try:
            job.cleanup()
        except Exception:
            printExc(f"Error during {job.stateName} cleanup:")
        disconnect(job.sigStateChanged, self.jobStateChanged)
        disconnect(job.sigFinished, self.jobFinished)
        if allowNextState and job.nextState is not None:
            self.requestStateChange(job.nextState, managerHandlesErrors=True)
