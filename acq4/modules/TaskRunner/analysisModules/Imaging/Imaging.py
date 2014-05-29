# -*- coding: utf-8 -*-
from acq4.modules.TaskRunner.analysisModules import AnalysisModule
from acq4.Manager import getManager
from PyQt4 import QtCore, QtGui
from imagingTemplate import Ui_Form
import numpy as np
import acq4.pyqtgraph as pg
import acq4.util.functions as fn
import acq4.util.metaarray as metaarray
from acq4.util.HelpfulException import HelpfulException
# import acq4.devices.Scanner.ScanUtilityFuncs as SUFA
from acq4.devices.Scanner.ScanProgram.rect import RectScan
from acq4.pyqtgraph.parametertree import ParameterTree, Parameter

class ImagingModule(AnalysisModule):
    def __init__(self, *args):
        AnalysisModule.__init__(self, *args)
        # self.ui = Ui_Form()
        # self.ui.setupUi(self)
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.splitter = QtGui.QSplitter()
        self.layout.addWidget(self.splitter)
        self.ptree = ParameterTree()
        self.splitter.addWidget(self.ptree)
        self.plotWidget = pg.ImageView()
        self.splitter.addWidget(self.plotWidget)

        # self.postGuiInit()

        self.params = Parameter(name='imager', children=[
            dict(name='scanner', type='interface', interfaceTypes=['scanner']),
            dict(name='detector', type='interface', interfaceTypes=['daqChannelGroup']),
            dict(name='decomb', type='float', value=20e-6, suffix='s', siPrefix=True, bounds=[0, 1e-3], step=1e-6, children=[
                dict(name='auto', type='bool', value=True)]),
            ])
        self.ptree.setParameters(self.params, showTop=False)

        self.man = getManager()
        self.lastFrame = None
        # self.SUF = SUFA.ScannerUtilities()
        # self.ui.alphaSlider.valueChanged.connect(self.imageAlphaAdjust)        
        self.img = None  ## image shown in camera module
        self.plotWidget.imageItem.setAutoDownsample(True)
        # self.ui.scannerComboBox.setTypes('scanner')
        # self.ui.detectorComboBox.setTypes('daqChannelGroup')
                
    def quit(self):
        AnalysisModule.quit(self)
        
    def saveState(self):
        return {'scanner': self.params['scanner'], 'detector': self.params['detector'], 'decomb': self.params['decomb'], 'decomb_auto': self.params['decomb', 'auto']}

    def restoreState(self, state):
        self.params['scanner'] = state['scanner']
        self.params['detector'] = state['detector']
        self.params['decomb'] = state['decomb']
        self.params['decomb', 'auto'] = state['decomb_auto']

    def taskSequenceStarted(self, *args):
        pass
    
    def taskFinished(self):
        pass
        
    def newFrame(self, frame):
        """
        Called when task is finished (truly completes, no errors/abort)
        frame contains all of the data returned from all devices
        """
        self.lastFrame = frame
        self.update()

    def update(self):
        frame = self.lastFrame
        if frame is None:
            self.clear()
            return
        # imageDownSample = self.ui.downSampling.value() # this is the "image" downsample,
        # get the downsample for the daq. This is far more complicated than it should be...

        # Get PMT signal
        pmt = frame['result'][self.params['detector']]["Channel":'Input']
        # info = finfo.infoCopy()
        # daqDownSample = info[1]['DAQ']['Input'].get('downsampling', 1)
        # if daqDownSample != 1:
            # raise HelpfulException("Set downsampling in DAQ to 1!")
        # get the data and the command used on the scanner
        pmtdata = pmt.asarray()
        t = pmt.xvals('Time')
        # dt = t[1]-t[0]

        progs = frame['cmd'][self.params['scanner']]['program']
        if len(progs) == 0:
            self.image.setImage(np.zeros((1,1)))
            return

        # For now, we only support single-component scan programs.
        prog = progs[0]
        # nscans = prog['nScans']
        # limits = prog['points']
        # dist = (pg.Point(limits[0])-pg.Point(limits[1])).length()
        # startT = prog['startTime']
        # endT = prog['endTime'] # note that this value is shared by all types, so rectscan computes in program generator...
        
        if prog['type'] == 'rect':
            rs = RectScan()
            rs.restoreState(prog['scanInfo'])
            imageData = rs.extractImage(pmtdata)
            imageData = imageData.transpose(0, 2, 1)  # Collected as (frame, row, col) but pg prefers images like (frame, col, row)

            if imageData.size == 0:
                self.clear()
                raise Exception('image Data has zero size')
            self.ui.plotWidget.setImage(imageData)
            # pts = prog['points']
            # floatpoints =[ (float(x[0]), float(x[1])) for x in pts]
            # width  = (pts[1] -pts[0]).length() # width is x in M
            # height = (pts[2]- pts[0]).length() # heigh in M
            self.ui.plotWidget.getView().setAspectLocked(True)
            self.ui.plotWidget.imageItem.setRect(QtCore.QRectF(0., 0., rs.width, rs.height))
            self.ui.plotWidget.autoRange()
            raise Exception()


        if prog['type'] == 'multipleLineScan': 
            totSamps = int(np.sum(prog['scanPointList'])) # samples per scan, before downsampling
            imageData = pmtdata[prog['startStopIndices'][0]:prog['startStopIndices'][0]+int((nscans*totSamps))].copy()           
            imageData = imageData.reshape(nscans, totSamps)
            csum = np.cumsum(prog['scanPointList'])
            for i in xrange(0, len(csum), 2):
                    imageData[:,csum[i]:csum[i+1]] = 0

            #imageData = imageData[:,0:prog['samplesPerScan']] # trim off the pause data
            imageData = fn.downsample(imageData, imageDownSample, axis=1)
            self.ui.plotWidget.setImage(imageData)
            self.ui.plotWidget.getView().setAspectLocked(False)
            self.ui.plotWidget.imageItem.setRect(QtCore.QRectF(startT, 0.0, totSamps*dt*nscans, dist ))
            self.ui.plotWidget.autoRange()
            storeFlag = frame['cmd']['protocol']['storeData'] # get flag 
            if storeFlag:
                dirhandle = frame['cmd']['protocol']['storageDir'] # grab directory
                self.info={'detector': self.detectorDevice(), 'scanner': self.scannerDevice(), 'indices': prog['startStopIndices'], 
                           'scanPointList': prog['scanPointList'], 'nscans': prog['nScans'], 
                           'positions': prog['points'],
                           'downSample': imageDownSample, 'daqDownSample': daqDownSample}
                info = [dict(name='Time', units='s', 
                             values=t[prog['startStopIndices'][0]:prog['startStopIndices'][1]-int(totSamps):int(totSamps)]), 
                        dict(name='Distance'), self.info]
                ma = metaarray.MetaArray(imageData, info=info)
                dirhandle.writeFile(ma, 'Imaging.ma')

        if prog['type'] == 'rectScan':
            samplesPerScan = prog['imageSize'][0]*prog['imageSize'][1]
            getManager().data = prog, pmtdata
            imageData = pmtdata[prog['startStopIndices'][0]:prog['startStopIndices'][0] + nscans*samplesPerScan]
            imageData=imageData.reshape(nscans, prog['imageSize'][1], prog['imageSize'][0])
            imageData = imageData.transpose(0,2,1)
            imageAve = np.mean(imageData, axis=0)
            #print prog['scanParameters']
            self.SUF.setScannerParameters(prog['scanParameters']) # load up information for Scanner calculations
            self.SUF.setScanInfo(prog['scanInfo'])
            imageAve, bestShift = self.SUF.adjustBidirectional(imageAve, True, 0.)
            #print 'bestShift: ', bestShift, ' microseconds'
            bestShift = 200e-6
            for i in range(nscans):
                (decombedImage, shift) = self.SUF.adjustBidirectional(imageData[i], False, bestShift)
                roImage = self.SUF.removeOverscan(decombedImage)
                if i == 0:
                    newImage = np.zeros((nscans, roImage.shape[0], roImage.shape[1]))
                newImage[i] = roImage
            #print imageAve.shape
            #print newImage.shape
            imageData = newImage
            

            # imageData = fn.downsample(imageData, imageDownSample, axis=0)
            if imageData.size == 0:
                raise Exception('image Data has zero size')
            self.ui.plotWidget.setImage(imageData)
            pts = prog['points']
            floatpoints =[ (float(x[0]), float(x[1])) for x in pts]
            width  = (pts[1] -pts[0]).length() # width is x in M
            height = (pts[2]- pts[0]).length() # heigh in M
            self.ui.plotWidget.getView().setAspectLocked(True)
            self.ui.plotWidget.imageItem.setRect(QtCore.QRectF(0., 0., width, height))
            self.ui.plotWidget.autoRange()
           # self.ui.histogram.imageChanged(autoLevel=True)
            #print 'rectscan - nscans, samplesperscan: ', prog['nScans'], samplesPerScan
            sd = self.pr.getDevice(self.scannerDevice())
            camMod = sd.cameraModule().window()
            if self.img is not None:
                camMod.removeItem(self.img)
                self.img = None
            self.img = pg.ImageItem(imageData.mean(axis=0))
            camMod.addItem(self.img)
            w = imageData.shape[1]
            h = imageData.shape[2]
            localPts = map(pg.Vector, [[0,0], [w,0], [0,h], [0,0,1]]) # w and h of data of image in pixels.
            globalPts = prog['points'] # sort of. - 
            m = pg.solve3DTransform(localPts, map(pg.Vector, globalPts+[[0,0,1]]))
            m[:,2] = m[:,3]
            m[2] = m[3]
            m[2,2] = 1
            tr = QtGui.QTransform(*m[:3,:3].transpose().reshape(9))
            self.img.setTransform(tr)
            storeFlag = frame['cmd']['protocol']['storeData'] # get flag 
           # print 'srttransform: ', pg.SRTTransform3D(tr)
            if storeFlag:
                dirhandle = frame['cmd']['protocol']['storageDir'] # grab directory
                self.info={'detector': self.detectorDevice(), 'scanner': self.scannerDevice(), 'indices': prog['startStopIndices'], 
                           'samplesPerScan': samplesPerScan, 'nscans': prog['nScans'], 
                           'positions': floatpoints, # prog['points'],
                           'downSample': imageDownSample,
                           'transform': pg.SRTTransform3D(tr),
                           }
                           
                # to line below, add x, y for the camera (look at camera video output)
                info = [dict(name='Time', units='s', 
                             values=t[prog['startStopIndices'][0]:prog['startStopIndices'][0]+nscans*samplesPerScan:samplesPerScan]), 
                        dict(name='Distance'), self.info]
                print self.info
                print info
                ma = metaarray.MetaArray(imageData, info=info)
                
                dirhandle.writeFile(ma, 'Imaging.ma')
        
    def clear(self):
        self.ui.plotWidget.clear()

        
    def imageAlphaAdjust(self):
        if self.img is None:
            return
        alpha = self.ui.alphaSlider.value()
        self.img.setImage(opacity=float(alpha/100.))
        
        
    def detectorDevice(self):
        return str(self.ui.detectorComboBox.currentText())
        
    def scannerDevice(self):
        return str(self.ui.scannerComboBox.currentText())
        
        

        