# -*- coding: utf-8 -*-
from __future__ import print_function
from acq4.util import Qt
import numpy as np
from acq4.devices.Device import *
from acq4.devices.OptomechDevice import *
from acq4.util.Mutex import Mutex
import acq4.pyqtgraph as pg


class Stage(Device, OptomechDevice):
    """Base class for mechanical stages with motorized control and/or position feedback.

    This is an optomechanical device that modifies its own transform based on position or orientation
    information received from a position control device. The transform is calculated as::

        totalTransform = baseTransform * stageTransform

    where *baseTransform* is defined in the configuration for the device, and *stageTransform* is
    defined by the hardware.
    """

    sigPositionChanged = Qt.Signal(object, object, object)  # self, new position, old position
    sigLimitsChanged = Qt.Signal(object)

    def __init__(self, dm, config, name):
        Device.__init__(self, dm, config, name)
        OptomechDevice.__init__(self, dm, config, name)

        # total device transform will be composed of a base transform (defined in the config)
        # and a dynamic translation provided by the hardware.
        self._baseTransform = Qt.QMatrix4x4(self.deviceTransform())
        self._stageTransform = Qt.QMatrix4x4()
        self._invStageTransform = Qt.QMatrix4x4()

        self.config = config
        self.lock = Mutex(Qt.QMutex.Recursive)

        nAxes = len(self.axes())
        self._lastPos = [0] * nAxes

        # default implementation just uses this matrix to
        # convert from device position to translation vector
        self._axisTransform = None
        self._inverseAxisTransform = None

        self._defaultSpeed = 'fast'
        self.setFastSpeed(config.get('fastSpeed', 1e-3))
        self.setSlowSpeed(config.get('slowSpeed', 10e-6))

        self._limits = [(None, None)] * nAxes

        self._progressDialog = None
        self._progressTimer = Qt.QTimer()
        self._progressTimer.timeout.connect(self.updateProgressDialog)

        dm.declareInterface(name, ['stage'], self)

    def quit(self):
        self.stop()

    def axes(self):
        """Return a tuple of axis names implemented by this device, like ('x', 'y', 'z').

        The axes described in the above data structure correspond to the mechanical
        actuators on the device; they do not necessarily correspond to the axes in the 
        global coordinate system or the local coordinate system of the device.

        This method must be reimplemented by subclasses.
        """
        raise NotImplementedError("Must be implemented in subclass.")

    def capabilities(self):
        """Return a structure describing the capabilities of this device::
        
            {
                'getPos': (x, y, z),      # bool: whether each axis can be read from the device
                'setPos': (x, y, z),      # bool: whether each axis can be set on the device
                'limits': (x, y, z),      # bool: whether limits can be set for each axis
            }
            
        The axes described in the above data structure correspond to the mechanical
        actuators on the device; they do not necessarily correspond to the axes in the 
        global coordinate system or the local coordinate system of the device.

        Subclasses must reimplement this method.
        """
        # todo: add other capability flags like resolution, speed, closed-loop, etc?
        raise NotImplementedError

    def setFastSpeed(self, v):
        """Set the maximum speed of the stage (m/sec) when under programmed control.
        """
        self.fastSpeed = v

    def setSlowSpeed(self, v):
        """Set the slow speed of the stage (m/sec) when under programmed control.

        This speed is used when it is necessary to minimize vibration or maximize movement accuracy.
        """
        self.slowSpeed = v

    def _interpretSpeed(self, speed):
        """Return a speed in m/s where the argument *speed* can be any of
        'fast', 'slow', or a float m/s.
        """
        if speed == 'fast':
            speed = self.fastSpeed
        elif speed == 'slow':
            speed = self.slowSpeed
        return speed

    def stageTransform(self):
        """Return the transform that implements the translation/rotation generated
        by the current hardware state. 
        """
        return pg.SRTTransform3D(self._stageTransform)

    def inverseStageTransform(self):
        if self._inverseStageTransform is None:
            inv, invertible = self.stageTransform().inverted()
            if not invertible:
                raise Exception("Transform is not invertible.")
            self._inverseStageTransform = inv
        return pg.SRTTransform3D(self._inverseStageTransform)

    def _makeStageTransform(self, pos):
        """Return a stage transform (as should be returned by stageTransform)
        and an optional inverse, given a position reported by the device.

        If the inverse transform is None, then it will be automatically generated
        on demand by calling transform.inverted().

        Subclasses may override this method; the default uses _axisTransform to 
        map from the device position to a 3D translation matrix. This covers only cases
        where the stage axes perform linear translations. For rotation or nonlinear
        movement, this method must be reimplemented.
        """
        tr = pg.SRTTransform3D()
        offset = pg.Vector(self.axisTransform().map(pg.Vector(pos)))
        tr.translate(offset)

        inv = pg.SRTTransform3D()
        inv.translate(-offset)

        return tr, inv

    def _solveStageTransform(self, pos_change):
        """Given a desired change of local origin, return the device position required.

        The default implementation simply inverts _axisTransform to generate this solution;
        devices with more complex kinematics need to reimplement this method.
        """ 
        tr = self.stageTransform().translation() + pos_change
        pos = self.inverseAxisTransform().map(tr)
        return pos

    def axisTransform(self):
        if self._axisTransform is None:
            self._axisTransform = pg.Transform3D()
            self._inverseAxisTransform = pg.Transform3D()
            scale = self.config.get('scale', None)
            if scale is not None:
                self._axisTransform.scale(*scale)
                self._inverseAxisTransform.scale(*[1.0 / x for x in scale])
        return pg.QtGui.QMatrix4x4(self._axisTransform)

    def inverseAxisTransform(self):
        if self._inverseAxisTransform is None:
            inv, invertible = self.axisTransform().inverted()[1]
            if not invertible:
                raise Exception("Transform is not invertible.")
            self._inverseAxisTransform = inv
        return pg.QtGui.QMatrix4x4(self._inverseAxisTransform)

    # def mapToStage(self, obj):
    #     return self._mapTransform(obj, self._stageTransform)

    # def mapFromStage(self, obj):
    #     return self._mapTransform(obj, self._invStageTransform)

    def posChanged(self, pos):
        """Handle device position changes by updating the device transform and
        emitting sigPositionChanged.

        Subclasses must call this method when the device position has changed.
        """
        with self.lock:
            lastPos = self._lastPos
            self._lastPos = pos
            self._stageTransform, self._inverseStageTransform = self._makeStageTransform(pos)
            self._updateTransform()

        self.sigPositionChanged.emit(self, pos, lastPos)

    def baseTransform(self):
        """Return the base transform for this Stage.
        """
        return Qt.QMatrix4x4(self._baseTransform)

    def setBaseTransform(self, tr):
        """Set the base transform of the stage. 

        This sets the starting position and orientation of the stage before the 
        hardware-reported stage position is taken into account.
        """
        self._baseTransform = Qt.QMatrix4x4(tr)
        self._updateTransform()

    def _updateTransform(self):
        ## this informs rigidly-connected devices that they have moved
        self.setDeviceTransform(self._baseTransform * self._stageTransform)

    def getPosition(self, refresh=False):
        """Return the position of the stage as reported by the controller.

        If refresh==False, the last known position is returned. Otherwise, the
        current position is requested from the controller. If request is True,
        then the position request may block if the device is currently busy.
        """
        if not refresh:
            with self.lock:
                return self._lastPos[:]
        else:
            return self._getPosition()

    def globalPosition(self):
        """Return the position of the local coordinate system origin relative to 
        the global coordinate system.
        """
        # note: the origin of the local coordinate frame is the center position of the device.
        return self.mapToGlobal([0, 0, 0])

    def _getPosition(self):
        """
        Must be reimplemented by subclass to re-read position from device.
        """
        raise NotImplementedError()

    def targetPosition(self):
        """If the stage is moving, return the target position. Otherwise return 
        the current position.
        """
        raise NotImplementedError()

    def globalTargetPosition(self):
        """Returns the target position mapped to the global coordinate system.

        See targetPosition().
        """
        # imagine what the global transform will look like after we reach the target..
        target = self.targetPosition()
        tr = self.baseTransform() * self._makeStageTransform(target)
        pd = self.parentDevice()
        if pd is not None:
            tr = pd.globalTransform() * tr
        return tr.map([0, 0, 0])

    def getState(self):
        with self.lock:
            return (self._lastPos[:],)

    def deviceInterface(self, win):
        return StageInterface(self, win)

    def setDefaultSpeed(self, speed):
        """Set the default speed of the device when moving.
        
        Generally speeds are specified approximately in m/s, although many 
        devices lack the capability to accurately set speed. This value may 
        also be 'fast' to indicate the device should move as quickly as 
        possible, or 'slow' to indicate the device should minimize vibrations
        while moving.        
        """
        if speed not in ('fast', 'slow'):
            speed = abs(float(speed))
        self._defaultSpeed = speed

    def isMoving(self):
        """Return True if the device is currently moving.
        """
        raise NotImplementedError()        

    def move(self, abs=None, rel=None, speed=None, progress=False, linear=False):
        """Move the device to a new position.
        
        Must specify either *abs* for an absolute position, or *rel* for a
        relative position. Either argument must be a sequence (x, y, z) with
        values in meters. Optionally, values may be None to indicate no 
        movement along that axis.
        
        If the *speed* argument is given, it temporarily overrides the default
        speed that was defined by the last call to setSpeed().
        
        If *progress* is True, then display a progress bar until the move is complete.

        If *linear* is True, then the movement is required to be in a straight line.

        Return a MoveFuture instance that can be used to monitor the progress 
        of the move.

        Note: the position must be expressed in the same coordinate system as returned 
        by getPosition().
        """
        if speed is None:
            speed = self._defaultSpeed
        if speed is None:
            raise TypeError("Must specify speed or set default speed before moving.")
        if abs is None and rel is None:
            raise TypeError("Must specify one of abs or rel arguments.")

        mfut = self._move(abs, rel, speed, linear=linear)

        if progress:
            self._progressDialog = Qt.QProgressDialog("%s moving..." % self.name(), None, 0, 100)
            self._progressDialog.mf = mfut
            self._progressTimer.start(100)

        return mfut
        
    def _move(self, abs, rel, speed, linear):
        """Must be reimplemented by subclasses and return a MoveFuture instance.
        """
        raise NotImplementedError()

    def moveToGlobal(self, pos, speed, linear=False):
        """Move the stage to a position expressed in the global coordinate frame.
        """
        localPos = self.mapFromGlobal(pos)
        stagePos = self._solveStageTransform(localPos)
        return self.moveTo(stagePos, speed, linear=linear)

    def _toAbsolutePosition(self, abs, rel):
        """Helper function to convert absolute or relative position (possibly 
        containing Nones) to an absolute position.
        """
        if rel is None:
            if any([x is None for x in abs]):
                pos = self.getPosition()
                for i,x in enumerate(abs):
                    if x is not None:
                        pos[i] = x
            else:
                pos = abs
        else:
            pos = self.getPosition()
            for i,x in enumerate(rel):
                if x is not None:
                    pos[i] += x
        return pos
        
    def moveBy(self, pos, speed, progress=False, linear=False):
        """Move by the specified relative distance. See move() for more 
        information.
        """
        return self.move(rel=pos, speed=speed, progress=progress, linear=linear)

    def moveTo(self, pos, speed, progress=False, linear=False):
        """Move to the specified absolute position. See move() for more 
        information.
        """
        return self.move(abs=pos, speed=speed, progress=progress, linear=linear)
    
    def stop(self):
        """Stop moving the device immediately.
        """
        raise NotImplementedError()

    def updateProgressDialog(self):
        done = int(self._progressDialog.mf.percentDone())
        self._progressDialog.setValue(done)
        if done == 100:
            self._progressTimer.stop()

    def setLimits(self, x=None, y=None, z=None):
        """Set the (min, max) position limits to enforce for each axis.

        Accepts keyword arguments 'x', 'y', 'z'; each supplied argument must be
        a (min, max) tuple where either value may be None to disable the limit.

        Note that some devices do not support limits.
        """
        changed = []
        for axis, limit in enumerate((x, y, z)):
            if limit is None:
                continue
            assert len(limit) == 2
            if self.capabilities()['limits'][axis] is not True:
                raise TypeError("Device does not support settings limits for axis %d." % axis)
            if tuple(self._limits[axis]) != tuple(limit):
                changed.append(axis)
                self._limits[axis] = tuple(limit)

        if len(changed) > 0:
            self.sigLimitsChanged.emit(changed)

    def getLimits(self):
        """Return a list the (min, max) position limits for each axis.
        """
        return self._limits[:]


class MoveFuture(object):
    """Used to track the progress of a requested move operation.
    """
    def __init__(self, dev, pos, speed):
        self.startTime = pg.ptime.time()
        self.dev = dev
        self.speed = speed
        self.targetPos = pos
        self.startPos = dev.getPosition()

    def percentDone(self):
        """Return the percent of the move that has completed.
        
        The default implementation calls getPosition on the device to determine
        the percent complete. Devices that do not provide position updates while 
        moving should reimplement this method.
        """
        if self.isDone():
            return 100
        s = np.array(self.startPos)
        t = np.array(self.targetPos)
        p = np.array(self.dev.getPosition())
        d1 = ((p - s)**2).sum()**0.5
        d2 = ((t - s)**2).sum()**0.5
        if d2 == 0:
            return 100
        return 100 * d1 / d2

    def wasInterrupted(self):
        """Return True if the move was interrupted before completing.
        """
        raise NotImplementedError()

    def isDone(self):
        """Return True if the move has completed or was interrupted.
        """
        return self.percentDone() == 100 or self.wasInterrupted()

    def errorMessage(self):
        """Return a string description of the reason for a move failure,
        or None if there was no failure (or if the reason is unknown).
        """
        return None
        
    def wait(self, timeout=None, updates=False):
        """Block until the move has completed, has been interrupted, or the
        specified timeout has elapsed.

        If *updates* is True, process Qt events while waiting.

        If the move did not complete, raise an exception.
        """
        start = ptime.time()
        while (timeout is None) or (ptime.time() < start + timeout):
            if self.isDone():
                break
            if updates is True:
                Qt.QTest.qWait(100)
            else:
                time.sleep(0.1)
        if not self.isDone() or self.wasInterrupted():
            err = self.errorMessage()
            if err is None:
                raise RuntimeError("Move did not complete.")
            else:
                raise RuntimeError("Move did not complete: %s" % err)


class StageInterface(Qt.QWidget):
    def __init__(self, dev, win):
        Qt.QWidget.__init__(self)
        self.win = win
        self.dev = dev

        self.layout = Qt.QGridLayout()
        self.setLayout(self.layout)
        self.axCtrls = {}
        self.posLabels = {}
        self.limitChecks = {}

        cap = dev.capabilities()
        self.nextRow = 0

        for axis, axisName in enumerate(self.dev.axes()):
            if cap['getPos'][axis]:
                axLabel = Qt.QLabel(axisName)
                axLabel.setMaximumWidth(15)
                posLabel = Qt.QLabel('0')
                self.posLabels[axis] = posLabel
                widgets = [axLabel, posLabel]
                if cap['limits'][axis]:
                    minCheck = Qt.QCheckBox('Min:')
                    minCheck.tag = (axis, 0)
                    maxCheck = Qt.QCheckBox('Max:')
                    maxCheck.tag = (axis, 1)
                    self.limitChecks[axis] = (minCheck, maxCheck)
                    widgets.extend([minCheck, maxCheck])
                    for check in (minCheck, maxCheck):
                        check.clicked.connect(self.limitCheckClicked)

                for i,w in enumerate(widgets):
                    self.layout.addWidget(w, self.nextRow, i)
                self.axCtrls[axis] = widgets
                self.nextRow += 1


        self.updateLimits()
        self.dev.sigPositionChanged.connect(self.update)
        self.dev.sigLimitsChanged.connect(self.updateLimits)
        self.update()

    def update(self):
        pos = self.dev.getPosition()
        for i in self.posLabels:
            text = pg.siFormat(pos[i], suffix='m', precision=5)
            self.posLabels[i].setText(text)

    def updateLimits(self):
        limits = self.dev.getLimits()
        cap = self.dev.capabilities()
        for axis in range(len(cap['limits'])):
            if not cap['limits'][axis]:
                continue
            for i,limit in enumerate(limits[axis]):
                check = self.limitChecks[axis][i]
                pfx = ('Min:', 'Max:')[i]
                if limit is None:
                    check.setText(pfx)
                    check.setChecked(False)
                else:
                    check.setText(pfx + ' %s' % pg.siFormat(limit, suffix='m'))
                    check.setChecked(True)

    def limitCheckClicked(self, b):
        check = self.sender()
        axis, minmax = check.tag
        limit = list(self.dev.getLimits()[axis])
        if b:
            limit[minmax] = self.dev.getPosition()[axis]
        else:
            limit[minmax] = None
        self.dev.setLimits(**{self.dev.axes()[axis]: tuple(limit)})


class StageHold(object):
    def __init__(self, stage):
        self.stage = stage

    def __enter__(self):
        self.stage.setHolding(True)
        return self

    def __exit__(self, *args):
        self.stage.setHolding(False)
