from .IControllerUnit import IControllerUnit
from .ContecOnOffActivation import ContecOnOffActivation
from .ContecBlindActivation import ContecBlindActivation
from .CommunicationManager import CommunicationManager
from .ContecConectivityConfiguration import ContecConectivityConfiguration
from .ActivationType import ActivationType
from .ContecActivation import ContecActivation
from .RegistersMapping import RegistersMapping
from threading import Lock

class ControllerUnit(IControllerUnit):
    _communicator: CommunicationManager
    _contecConfiguration: ContecConectivityConfiguration
    _activations: list[ContecActivation]
    _lock: Lock = Lock()
    ActivationsRegister: int = 0
    NumberOfActivations: int = 8

    def __init__(self, contecConfiguration: ContecConectivityConfiguration, communicator: CommunicationManager, unitId: int) -> None:
        self.__UnitId = unitId
        self._communicator = communicator
        self._contecConfiguration = contecConfiguration
        self.IsHealthy = False
        self._activations = []

    @property
    def UnitId(self) -> int:
        return self.__UnitId

    @property
    def IsHealthy(self) -> bool:
        return self.__IsHealthy

    @IsHealthy.setter
    def IsHealthy(self, var) -> None:
        self.__IsHealthy = var
        #lock (_lock)
        #{
        #    foreach (ContecActivation activation in _activations)
        #    {
        #        activation.SetHealth(_isHealthy);
        #    }
        #}
    
    def AddExistingActivation(self, contecActivation: ContecActivation) -> None:
        self._lock.acquire()
        try:
            self._activations.append(contecActivation)
        finally:
            self._lock.release()

    async def UpdateCurrentStatus(self) -> None:
        registers = await self._communicator.ReadInputRegistersAsync(self.UnitId, RegistersMapping.ActivationsState, 3)
        if len(registers) != 3:
            raise Exception("Unexpected number of registers")
        
        # Saving the current ActivationsRegister so when we need to change the activation state,
        # we will change only the desired state, while leaving the rest of the states as is.
        self.ActivationsRegister = registers[0]
        self._lock.acquire()
        try:
            for activation in self._activations:
                activation.ParseStateRegisters(registers)
        finally:
            self._lock.release()
    
    async def ChangeActivationRegister(self, mask: int, shouldTurnOn: bool) -> None:
        if shouldTurnOn:
            self.ActivationsRegister = self.ActivationsRegister | mask
        else:
            self.ActivationsRegister = self.ActivationsRegister & (~mask)
        await self.SetRegisterValue(RegistersMapping.ActivationsState, self.ActivationsRegister)
        
    async def SetRegisterValue(self, registerNumber: int, value: int) -> None:
        await self._communicator.WriteSingleRegisterAsync(self.UnitId, registerNumber, value)

    async def DiscoverAsync(self) -> list[ContecActivation]:
        registers: list[int] = await self._communicator.ReadInputRegistersAsync(self.UnitId, 10, self.NumberOfActivations * 2)
        allActivations: list[ContecActivation] = []
        self._lock.acquire()
        try:
            i = 0
            while i < self.NumberOfActivations:
                try:
                    isBlind = registers[1 + (i * 2)] > 0
                    if isBlind:
                        # First, sanity check. For blinds, i must be even number.
                        if (i % 2) != 0:
                            print(f"Try to set up Contec blind with odd activation number {i}.")
                            continue

                        # Make sure we don't already have any entity in the following activation.
                        if any(contecActivation.StartActivationNumber == i + 1 for contecActivation in self._activations):
                            print(f"While trying to set up Contec blind for activation {i}, found already existing activation in the next odd number {i + 1}.")
                            continue

                        activation: ContecActivation = next((activation for activation in self._activations if activation.StartActivationNumber == i), None)
                        if activation != None:
                            # We already have this entity. Just make sure it's of blind type.
                            if activation.ActivationType != ActivationType.Blind:
                                print(f"While discovering blind in activation {i}, we found already existing activation of type {activation.ActivationType}")
                        
                            continue

                        # Add this blind activation.
                        allActivations.append(ContecBlindActivation(i, self))
                        i += 1

                    else:
                        activation: ContecActivation = next((activation for activation in self._activations if activation.StartActivationNumber == i), None)
                        if activation != None:
                            # We already have this entity. Just make sure it's of blind type.
                            if activation.ActivationType != ActivationType.OnOff:
                                print(f"While discovering on-off in activation {i}, we found already existing activation of type {activation.ActivationType}")
                        
                            continue

                        allActivations.append(ContecOnOffActivation(i, self))
                finally:
                    i += 1
            
            # Sanity check - The logic built in a way that we should discover everything once. We can't discover only half of the
            # activations, and later discover the rest. So we should check that if we found something, we don't already have any
            # activation, and vice versa.
            if len(allActivations) != 0 and self._activations != None and len(self._activations) > 0:
                message: str = f"Illegal state! Contec controller {self.UnitId} discovered {allActivations.Count} new activations, while there are already {self._activations.Count} existing activations."
                print(message)
                raise Exception(message)
            
            for contecActivation in allActivations:
                self._activations.append(contecActivation)

        finally:
            self._lock.release()
        
        print(f"Done creating controller {self.UnitId} activations")
        return allActivations

        