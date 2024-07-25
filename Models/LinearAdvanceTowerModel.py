# Import the correct version of PyQt
try:
    from PyQt6.QtCore import pyqtSignal, pyqtProperty
except ImportError:
    from PyQt5.QtCore import pyqtSignal, pyqtProperty
    
import os

from UM.Logger import Logger
from UM.i18n import i18nCatalog
from UM.Resources import Resources

from .ModelBase import ModelBase

Resources.addSearchPath(
    os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'),'Resources')
)  # Plugin translation file import
catalog = i18nCatalog("autotowers")

class LinearAdvanceTowerModel(ModelBase):

    # The available pa tower presets
    _presetsTable = [
        {'name': catalog.i18nc("@model", "K-factor 0.0 - 0.2") , 'filename': 'Linear Advance Tower - K 0.0-0.2.stl', 'start K': '0.0', 'K change': '0.02'},
        {'name': catalog.i18nc("@model", "K-factor - 0.0 - 2.0") , 'filename': 'Linear Advance Tower - K 0.0-2.0.stl', 'start K': '0.0', 'K change': '0.2'},
    ]


    # Make the presets availabe to QML
    presetsModelChanged = pyqtSignal()

    @pyqtProperty(list, notify=presetsModelChanged)
    def presetsModel(self):
        return self._presetsTable



    # The selected fan tower preset index
    _presetIndex = 0

    presetIndexChanged = pyqtSignal()

    def setPresetIndex(self, value)->None:
        self._presetIndex = int(value)
        self.presetIndexChanged.emit()

    @pyqtProperty(int, notify=presetIndexChanged, fset=setPresetIndex)
    def presetIndex(self)->int:
        return self._presetIndex
    
    @pyqtProperty(bool, notify=presetIndexChanged)
    def presetSelected(self)->bool:
        return self._presetIndex < len(self._presetsTable)
    
    @pyqtProperty(str, notify=presetIndexChanged)
    def presetName(self)->str:
        return self._presetsTable[self.presetIndex]['name']
    
    @pyqtProperty(str, notify=presetIndexChanged)
    def presetFileName(self)->str:
        return self._presetsTable[self.presetIndex]['filename']
    
    @pyqtProperty(str, notify=presetIndexChanged)
    def presetFilePath(self)->str:
        return self._buildStlFilePath(self.presetFileName)
    
    @pyqtProperty(str, notify=presetIndexChanged)
    def presetStartKfactorStr(self)->str:
        return self._presetsTable[self.presetIndex]['start K']
    
    @pyqtProperty(float, notify=presetIndexChanged)
    def presetStartKfactor(self)->float:
        return float(self.presetStartKfactorStr)
    
    @pyqtProperty(str, notify=presetIndexChanged)
    def presetKfactorChangeStr(self)->str:
        return self._presetsTable[self.presetIndex]['K change']
    
    @pyqtProperty(float, notify=presetIndexChanged)
    def presetKfactorChange(self)->float:
        return float(self.presetKfactorChangeStr)
    


    # The icon to display on the dialog
    dialogIconChanged = pyqtSignal()

    @pyqtProperty(str, notify=dialogIconChanged)
    def dialogIcon(self)->str:
        return 'latower_icon.png'



    # The starting K-factor value for the tower
    _startKfactorStr = '0.0'

    startKfactorStrChanged = pyqtSignal()
    
    def setStartKfactorStr(self, value)->None:
        self._startKfactorStr = value
        self.startKfactorStrChanged.emit()

    @pyqtProperty(str, notify=startKfactorStrChanged, fset=setStartKfactorStr)
    def startKfactorStr(self)->str:
        # Allow the preset to override this setting
        if self.presetSelected:
            return self.presetStartKfactorStr
        else:
            return self._startKfactorStr

    @pyqtProperty(float, notify=startKfactorStrChanged)
    def startKfactor(self)->float:
        return float(self.startKfactorStr)



    # The ending K-factor value for the tower
    _endKfactorStr = '0.2'

    endKfactorStrChanged = pyqtSignal()
    
    def setEndKfactorStr(self, value)->None:
        self._endKfactorStr = value
        self.endKfactorStrChanged.emit()

    @pyqtProperty(str, notify=endKfactorStrChanged, fset=setEndKfactorStr)
    def endKfactorStr(self)->str:
        return self._endKfactorStr

    @pyqtProperty(float, notify=endKfactorStrChanged)
    def endKfactor(self)->float:
        return float(self.endKfactorStr)



    # The amount to change the K-factor between tower sections
    _kfactorChangeStr = '0.02'

    kfactorChangeStrChanged = pyqtSignal()
    
    def setKfactorChangeStr(self, value)->None:
        self._kfactorChangeStr = value
        self.kfactorChangeStrChanged.emit()

    @pyqtProperty(str, notify=kfactorChangeStrChanged, fset=setKfactorChangeStr)
    def kfactorChangeStr(self)->str:
        # Allow the preset to override this setting
        if self.presetSelected:
            return self.presetKfactorChangeStr
        else:
            return self._kfactorChangeStr

    @pyqtProperty(float, notify=kfactorChangeStrChanged)
    def kfactorChange(self)->float:
        return float(self.kfactorChangeStr)



    # The label to add to the tower
    _towerLabel = ''

    towerLabelChanged = pyqtSignal()
    
    def setTowerLabel(self, value)->None:
        self._towerLabel = value
        self.towerLabelChanged.emit()

    @pyqtProperty(str, notify=towerLabelChanged, fset=setTowerLabel)
    def towerLabel(self)->str:
        return self._towerLabel



    # The description to carve up the side of the tower
    _towerDescription = 'K-factor'

    towerDescriptionChanged = pyqtSignal()
    
    def setTowerDescription(self, value)->None:
        self._towerDescription = value
        self.towerDescriptionChanged.emit()

    @pyqtProperty(str, notify=towerDescriptionChanged, fset=setTowerDescription)
    def towerDescription(self)->str:
        return self._towerDescription
    


    def __init__(self, stlDir):
        super().__init__(stlDir=stlDir)
