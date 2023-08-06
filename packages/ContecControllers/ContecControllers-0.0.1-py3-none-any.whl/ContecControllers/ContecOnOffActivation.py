
from .ContecActivation import ContecActivation
from .ActivationType import ActivationType
from .IControllerUnit import IControllerUnit

class ContecOnOffActivation(ContecActivation):

    def __init__(self, activationNumber: int, controllerUnit: IControllerUnit) -> None:
        super().__init__(activationNumber, controllerUnit, ActivationType.OnOff)
        self.__IsOn = False

    @property
    def IsOn(self) -> bool:
        return self.__IsOn
    
    def SetNewState(self, isOn: bool):
        if self.IsOn != isOn:
            self.__IsOn = isOn
            #StateChanged?.Invoke(IsOn);

        #SignalRefresh();

    def ParseStateRegisters(self, stateRegisters: list[int]) -> None:
        activationsPushersState, activationsOnOffState = stateRegisters[0].to_bytes(2, "big")
        isOn: bool = ContecActivation.IsByteOn(activationsOnOffState, self.StartActivationNumber)
        self.SetNewState(isOn)