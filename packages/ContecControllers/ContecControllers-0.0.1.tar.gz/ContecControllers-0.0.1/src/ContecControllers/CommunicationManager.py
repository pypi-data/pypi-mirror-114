from .Conductor import Conductor
from typing import Callable
from pymodbus.client.sync import ModbusTcpClient
import asyncio
from queue import Queue
from pymodbus.exceptions import ModbusIOException
import time

class CommunicationManager:
    _pendingTasks = Queue
    _controllersIp: str
    _controllersPort: int
    _modbusTcpClient: ModbusTcpClient
    _conductor: Conductor
    _workerTask: asyncio.Task

    def __init__(self, controllersIp: str, controllersPort: int) -> None:
        self._controllersIp = controllersIp
        self._controllersPort = controllersPort
        self._modbusTcpClient = ModbusTcpClient(self._controllersIp, self._controllersPort)
        self._conductor = Conductor()
        self._pendingTasks = Queue()

    def StartListening(self) -> None:
        self._workerTask = asyncio.create_task(self._ExecutePendingCommand())

    async def ReadInputRegistersAsync(self, slaveAddress: int, startAddress: int, numberOfPoints: int) -> list[int]:
        result = [None]
        func = lambda: self._ReadInputRegisters(slaveAddress, startAddress, numberOfPoints, result)
        taskToExecute = TaskToExecute(func)
        self._pendingTasks.put(taskToExecute)
        await taskToExecute.TaskToComplete
        return result[0]
    
    async def WriteSingleRegisterAsync(self, slaveAddress, regAddress, newRegValue) -> None:
        func = lambda: self._WriteSingleRegisterAsync(slaveAddress, regAddress, newRegValue)
        taskToExecute = TaskToExecute(func)
        self._pendingTasks.put(taskToExecute)
        await taskToExecute.TaskToComplete

    async def CloseAsync(self) -> None:
        self._workerTask.cancel()

    def _ReadInputRegisters(self, slaveAddress: int, startAddress: int, numberOfPoints: int, result: list) -> None:
        res = self._modbusTcpClient.read_holding_registers(startAddress, numberOfPoints, unit=(slaveAddress + 1))
        if type(res) is ModbusIOException:
            raise res
        result[0] = res.registers

    def _WriteSingleRegisterAsync(self, slaveAddress, regAddress, newRegValue) -> None:
        res = self._modbusTcpClient.write_register(regAddress, newRegValue, unit=(slaveAddress + 1))
        if type(res) is ModbusIOException:
            raise res

    async def _ExecutePendingCommand(self) -> None:
        while True:
            try:
                await asyncio.sleep(0.03) # 30 ms
                ticket = self._conductor.TryObtainTicket()
                if ticket == None:
                    return
                with ticket:
                    taskToExecute: TaskToExecute = self._pendingTasks.get()
                    if taskToExecute == None:
                        continue
                    while not self._modbusTcpClient.is_socket_open():
                        if self.IsClosed():
                            return
                        if not self._modbusTcpClient.connect():
                            print("Failed to connect to controllers")
                            await asyncio.sleep(1)

                    try:
                        taskToExecute.FunctionToPerforme()
                        taskToExecute.TaskToComplete.set_result(True)
                    except Exception as e:
                        print(e)
                        self._pendingTasks.put(taskToExecute)
            except Exception as e:
                pass
    
    def IsClosed(self):
        ticket = self._conductor.TryObtainTicket()
        if ticket == None:
            return True
        with ticket:
            return False

class TaskToExecute:
    def __init__(self, functionToPerforme: Callable[[], any]):
        self.__FunctionToPerforme = functionToPerforme
        self.__TaskToComplete = asyncio.Future()

    @property
    def FunctionToPerforme(self) -> Callable[[], any]:
        return self.__FunctionToPerforme

    @property
    def TaskToComplete(self) -> asyncio.Future:
        return self.__TaskToComplete

async def Main():
    communicationManager = CommunicationManager('127.0.0.1', 1234)
    communicationManager.StartListening()
    for i in range(1000):
        await communicationManager.WriteSingleRegisterAsync(1, 26, i % 10)
        res = await communicationManager.ReadInputRegistersAsync(1, 26, 3)
        print(f"got result {i} - {res}")
        time.sleep(1)
    await communicationManager.CloseAsync()
    print("Done")
    await asyncio.sleep(5)
    print("Done5")

if __name__ == "__main__":
    asyncio.run(Main())