from .igorpro import IgorThread
from PyQt4 import QtCore


def __reload__(old):
    MIES._bridge = old['MIESBridge']._bridge


class MIES(QtCore.QObject):
    """Bridge for communicating with MIES (multi-patch ephys and pressure control in IgorPro)
    """
    dataReady = QtCore.Signal()
    _bridge = None

    @classmethod
    def getBridge(cls, useZMQ=False):
        """Return a singleton MIESBridge instance.
        """
        # TODO: Handle switching between ZMQ and ActiveX?
        if cls._bridge is None:
            cls._bridge = MIES(useZMQ=useZMQ)
        return cls._bridge

    def __init__(self, useZMQ=False):
        self.igor = IgorThread(useZMQ)
        self.usingZMQ = useZMQ
        self.windowName = 'ITC1600_Dev_0'
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.getMIESUpdate)
        self.updateTimer.start(200)

    def getMIESUpdate(self):
        if self.usingZMQ:
            data = self.igor("FFI_ReturnTPValues")
            self.processUpdate(data)
            return data
        else:
            raise RuntimeError("getMIESUpdate not supported in ActiveX")

    def processUpdate(self, data):
        pass

    def resetData(self):
        pass

    def selectHeadstage(self, hs):
        return self.setCtrl("slider_DataAcq_ActiveHeadstage", hs)

    def setManualPressure(self, pressure):
        return self.setCtrl("setvar_DataAcq_SSPressure", pressure)

    def setApproach(self, hs):
        windowName = '"{}"'.format(self.windowName)
        return self.igor("P_MethodApproach", windowName, hs)
        #return self.setCtrl("button_DataAcq_Approach")

    def setSeal(self):
        windowName = '"{}"'.format(self.windowName)
        return self.igor("P_MethodSeal", windowName, hs)
        #return self.setCtrl("button_DataAcq_Seal")

    def setHeadstageActive(self, hs, active):
        return self.setCtrl('Check_DataAcqHS_%02d' % hs, active)

    def autoPipetteOffset(self):
        return self.setCtrl('button_DataAcq_AutoPipOffset_VC')

    def setCtrl(self, name, value=None):
        """Set or activate a GUI control in MIES.
        """
        windowName = '"{}"'.format(self.windowName)
        name_arg = '"{}"'.format(name)
        if value is None:
            return self.igor('PGC_SetAndActivateControl', windowName, name_arg)
        else:
            return self.igor('PGC_SetAndActivateControlVar', windowName, name_arg, value)

    def __del__(self):
        self.updateTimer.stop()
        super(MIES, self).__del__()
