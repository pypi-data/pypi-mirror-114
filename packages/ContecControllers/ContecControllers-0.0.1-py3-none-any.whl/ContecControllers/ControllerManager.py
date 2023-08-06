import asyncio
from .CommunicationManager import CommunicationManager
from .ContecConectivityConfiguration import ContecConectivityConfiguration
from .ControllersStatusReader import ControllersStatusReader
from .ControllerUnit import ControllerUnit
from .ActivationType import ActivationType
from .ContecOnOffActivation import ContecOnOffActivation
from .ContecBlindActivation import ContecBlindActivation

class ControllerManager:
    _controllerUnits: list[ControllerUnit]
    _controllersStatusReader: ControllersStatusReader
    _contecConectivityConfiguration: ContecConectivityConfiguration
    _communicationManager: CommunicationManager

    def __init__(self, contecConectivityConfiguration: ContecConectivityConfiguration) -> None:
        self._contecConectivityConfiguration = contecConectivityConfiguration
        self._communicationManager = CommunicationManager(self._contecConectivityConfiguration.ControllerIp, self._contecConectivityConfiguration.ControllerPort)
        #CommunicationManager.ConnectionEstablished += ConnectionEstablished;
        #CommunicationManager.ConnectionLost += ConnectionLost;
        self._controllerUnits = []
        for i in range(self._contecConectivityConfiguration.NumberOfControllers):
            self._controllerUnits.append(ControllerUnit(self._contecConectivityConfiguration, self._communicationManager, i))
        
        self._controllersStatusReader = ControllersStatusReader(self._contecConectivityConfiguration, self._controllerUnits)
        self.__OnOffActivations = []
        self.__BlindActivations = []
    
    @property
    def OnOffActivations(self)-> list[ContecOnOffActivation]:
        return self.__OnOffActivations
    
    @property
    def BlindActivations(self)-> list[ContecBlindActivation]:
        return self.__BlindActivations

    async def CloseAsync(self) -> None:
        await self._controllersStatusReader.Close()
        #CommunicationManager.ConnectionEstablished -= ConnectionEstablished;
        #CommunicationManager.ConnectionLost -= ConnectionLost;
        await self._communicationManager.CloseAsync()
    
    def Init(self) -> None:
        self._communicationManager.StartListening()

    #async def SetEntitiesFromDatabaseAsync

    async def DiscoverEntitiesAsync(self) -> None:
        for controllerUnit in self._controllerUnits:
            newActivations = await controllerUnit.DiscoverAsync()
            print(f"Discovered {len(newActivations)} activations in controller {controllerUnit.UnitId}.")
            for activation in newActivations:
                if activation.ActivationType == ActivationType.Blind:
                    self.__BlindActivations.append(activation)
                else:
                    self.__OnOffActivations.append(activation)

async def Main() -> None:
    controllerManager = ControllerManager(ContecConectivityConfiguration(2, '127.0.0.1', 1234))
    controllerManager.Init()
    await controllerManager.DiscoverEntitiesAsync()
    onOffActivations: list[ContecOnOffActivation] = controllerManager.OnOffActivations
    blindActivations: list[ContecBlindActivation] = controllerManager.BlindActivations
    print(f"onOff - {len(onOffActivations)}. Blind - {len(blindActivations)}")
    import os
    clear = lambda: os.system('cls')
    for i in range(100):
        await asyncio.sleep(1)
        clear()
        for onOff in onOffActivations:
            print(f"[OnOff] - {onOff.ControllerUnit.UnitId}-{onOff.StartActivationNumber} - {onOff.IsOn}")
        for blind in blindActivations:
            print(f"[Blind] - {blind.ControllerUnit.UnitId}-{blind.StartActivationNumber} - {blind.MovingDirection} ({blind.BlindOpeningPercentage}%)")

if __name__ == "__main__":
    asyncio.run(Main())