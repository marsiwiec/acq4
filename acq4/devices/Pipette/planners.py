import numpy as np


def defaultMotionPlanners():
    return {
        'home': HomeMotionPlanner,
        'search': SearchMotionPlanner,
        'aboveTarget': AboveTargetMotionPlanner,
        'approach': ApproachMotionPlanner,
        'target': TargetMotionPlanner,
        # 'clean': CleanMotionPlanner,
        # 'rinse': RinseMotionPlanner,
        'idle': IdleMotionPlanner,
    }


class PipetteMotionPlanner(object):
    def __init__(self, pip, position, speed, **kwds):
        self.pip = pip
        self.position = position
        self.speed = speed
        self.kwds = kwds

        self.future = None

    def move(self):
        """Move the pipette to the requested named position and return a Future 
        """
        if self.future is not None:
            self.stop()

        self.future = self._move()

    def stop(self):
        if self.future is not None:
            self.future.stop()

    def _move(self):
        raise NotImplememtedError()


class HomeMotionPlanner(PipetteMotionPlanner):
    """Extract pipette tip diagonally, then move stage to home position.
    """
    def _move(self):
        pip = self.pip
        speed = self.speed
        stage = pip.parentDevice()
        stagePos = stage.globalPosition()
        stageHome = stage.homePosition()
        globalMove = np.asarray(stageHome) - np.asarray(stagePos) # this is how much electrode should move in global coordinates

        startPosGlobal = pip.globalPosition()
        endPosGlobal = np.asarray(startPosGlobal) + globalMove  # this is where electrode should end up in global coordinates
        endPos = pip.mapFromGlobal(endPosGlobal)  # and in local coordinates

        # define the path to take in local coordinates because that makes it
        # easier to do the boundary intersections
        homeAngle = np.arctan2(endPos[2], -endPos[0])
        if homeAngle > pip.pitchRadians():
            # diagonal move to 
            dz = -endPos[0] * np.tan(pip.pitchRadians())
            waypoint = pip.mapToGlobal([endPos[0], 0, dz])
        else:
            dx = -endPos[2] / np.tan(pip.pitchRadians())
            waypoint = pip.mapToGlobal([dx, 0, endPos[2]])
            if dx > 0:  # in case home z position is below the current z pos.
                waypoint = None
        
        if waypoint is None:
            path = [(endPosGlobal, speed, False)]
        else:
            # sanity check
            for i in range(3):
                waypoint[i] = np.clip(waypoint[i], startPosGlobal[i], endPosGlobal[i])
            path = [
                (waypoint, speed, True),
                (endPosGlobal, speed, False),
            ]

        return pip._movePath(path)


class SearchMotionPlanner(PipetteMotionPlanner):
    """Focus the microscope 2mm above the surface, then move the electrode 
    tip to 500um below the focal point of the microscope. 

    This position is used when searching for new electrodes.

    Set *distance* to adjust the search position along the pipette's x-axis. Positive values
    move the tip farther from the microscope center to reduce the probability of collisions.
    Negative values move the pipette past the center of the microscope to improve the
    probability of seeing the tip immediately. 
    """
    def _move(self):
        pip = self.pip
        speed = self.speed
        distance = self.kwds.get('distance', 0)

        # Bring focus to 2mm above surface (if needed)
        scope = pip.scopeDevice()
        surfaceDepth = scope.getSurfaceDepth()
        if surfaceDepth is None:
            raise Exception("Cannot determine search position; surface depth is not defined.")
        searchDepth = surfaceDepth + pip._opts['searchHeight']

        cam = pip.imagingDevice()
        focusDepth = cam.getFocusDepth()

        # move scope such that camera will be focused at searchDepth
        if focusDepth < searchDepth:
            scopeFocus = scope.getFocusDepth()
            scope.setFocusDepth(scopeFocus + searchDepth - focusDepth).wait(updates=True)

        # Here's where we want the pipette tip in global coordinates:
        globalTarget = cam.globalCenterPosition('roi')
        globalTarget[2] += pip._opts['searchTipHeight'] - pip._opts['searchHeight']

        # adjust for distance argument:
        localTarget = pip.mapFromGlobal(globalTarget)
        localTarget[0] -= distance
        globalTarget = pip.mapToGlobal(localTarget)

        return pip._moveToGlobal(globalTarget, speed)


class TargetMotionPlanner(PipetteMotionPlanner):
    def _move(self):
        pip = self.pip
        speed = self.speed

        target = pip.targetPosition()
        pos = pip.globalPosition()
        if np.linalg.norm(np.asarray(target) - pos) < 1e-7:
            return
        path = pip._approachPath(target, speed)
        path.append([target, 100e-6, True])
        return pip._movePath(path)


class ApproachMotionPlanner(PipetteMotionPlanner):
    def _move(self):
        pip = self.pip
        speed = self.speed

        target = pip.targetPosition()
        return pip._movePath(pip._approachPath(target, speed))
    
    def _approachPath(self, target, speed):
        # Return steps (in global coords) needed to move to approach position
        stbyDepth = self.approachDepth()
        pos = self.globalPosition()

        # steps are in global coordinates.
        path = []

        # If tip is below the surface, then first pull out slowly along pipette axis
        if pos[2] < stbyDepth:
            dz = stbyDepth - pos[2]
            dx = -dz / np.tan(self.pitchRadians())
            last = np.array([dx, 0., dz])
            path.append([self.mapToGlobal(last), 100e-6, True])  # slow removal from sample
        else:
            last = np.array([0., 0., 0.])

        # local vector pointing in direction of electrode tip
        evec = np.array([1., 0., -np.tan(self.pitchRadians())])
        evec /= np.linalg.norm(evec)

        # target in local coordinates
        ltarget = self.mapFromGlobal(target)

        # compute approach position (axis aligned to target, at standby depth or higher)
        dz2 = max(0, stbyDepth - target[2])
        dx2 = -dz2 / np.tan(self.pitchRadians())
        stby = ltarget + np.array([dx2, 0., dz2])

        # compute intermediate position (point along approach axis that is closest to the current position)
        targetToTip = last - ltarget
        targetToStby = stby - ltarget
        targetToStby /= np.linalg.norm(targetToStby)
        closest = ltarget + np.dot(targetToTip, targetToStby) * targetToStby

        if np.linalg.norm(stby - last) > 1e-6:
            if (closest[2] > stby[2]) and (np.linalg.norm(stby - closest) > 1e-6):
                path.append([self.mapToGlobal(closest), speed, True])
            path.append([self.mapToGlobal(stby), speed, True])

        return path


class AboveTargetMotionPlanner(PipetteMotionPlanner):
    """Move the pipette tip to be centered over the target in x/y, and 100 um above
    the sample surface in z. 

    This position is used to recalibrate the pipette immediately before going to approach.
    """
    def _move(self):
        pip = self.pip
        speed = self.speed

        scope = pip.scopeDevice()
        waypoint1, waypoint2 = pip.aboveTargetPath()

        pfut = pip._moveToGlobal(waypoint1, speed)
        sfut = scope.setGlobalPosition(waypoint2)
        pfut.wait(updates=True)
        pip._moveToGlobal(waypoint2, 'slow').wait(updates=True)
        sfut.wait(updates=True)

    def aboveTargetPath(self):
        """Return the path to the "above target" recalibration position.

        The path has 2 waypoints:

        1. 100 um away from the second waypoint, on a diagonal approach. This is meant to normalize the hysteresis
           at the second waypoint. 
        2. This position is centered on the target, a small distance above the sample surface.
        """
        target = self.targetPosition()

        # will recalibrate 50 um above surface
        scope = self.scopeDevice()
        surfaceDepth = scope.getSurfaceDepth()
        waypoint2 = np.array(target)
        waypoint2[2] = surfaceDepth + 50e-6

        # Need to arrive at this point via approach angle to correct for hysteresis
        lwp = self.mapFromGlobal(waypoint2)
        dz = 100e-6
        lwp[2] += dz
        lwp[0] -= dz / np.tan(self.pitchRadians())
        waypoint1 = self.mapToGlobal(lwp)

        return waypoint1, waypoint2


class IdleMotionPlanner(PipetteMotionPlanner):
    """Move the electrode tip to the outer edge of the recording chamber, 1mm above the sample surface.

    NOTE: this method assumes that (0, 0) in global coordinates represents the center of the recording
    chamber.
    """
    def _move(self):
        pip = self.pip
        speed = self.speed

        scope = pip.scopeDevice()
        surface = scope.getSurfaceDepth()
        if surface is None:
            raise Exception("Surface depth has not been set.")

        # we want to land 1 mm above sample surface
        idleDepth = surface + pip._opts['idleHeight']

        # If the tip is below idle depth, bring it up along the axis of the electrode.
        pos = pip.globalPosition()
        if pos[2] < idleDepth:
            pip.advance(idleDepth, speed)

        # From here, move directly to idle position
        angle = pip.yawRadians()
        ds = pip._opts['idleDistance']  # move to 7 mm from center
        globalIdlePos = -ds * np.cos(angle), -ds * np.sin(angle), idleDepth
        pip._moveToGlobal(globalIdlePos, speed)
