import asyncio
from asyncio.tasks import sleep
from .ControllerUnit import ControllerUnit
from .Conductor import Conductor, Ticket
from .ContecConectivityConfiguration import ContecConectivityConfiguration

class ControllersStatusReader:
    _controllerUnits: list[ControllerUnit]
    _contecConfiguration: ContecConectivityConfiguration
    _conductor: Conductor = Conductor()
    _currentControllerIndex: int = 0
    _workerTask: asyncio.Task

    def __init__(self, contecConfiguration: ContecConectivityConfiguration, controllerUnits: list[ControllerUnit]) -> None:
        self._controllerUnits = controllerUnits
        self._contecConfiguration = contecConfiguration
        self._workerTask = asyncio.create_task(self._UpdateNextController())

    async def Close(self) -> None:
        await self._conductor.Close()
        self._workerTask.cancel()

    async def _UpdateNextController(self) -> None:
        while True:
            try:
                ticket: Ticket = self._conductor.TryObtainTicket()
                if ticket == None:
                    print("Conductor closed")
                    return
                
                with ticket:
                    unit: ControllerUnit = self._controllerUnits[self._currentControllerIndex]
                    await unit.UpdateCurrentStatus()
                    self._currentControllerIndex += 1
                    if self._currentControllerIndex >= self._contecConfiguration.NumberOfControllers:
                        self._currentControllerIndex = 0
            except Exception as ex:
                print(f"Failed to read controller {self._currentControllerIndex} status: {ex}")
            
            sleep(0.05)

