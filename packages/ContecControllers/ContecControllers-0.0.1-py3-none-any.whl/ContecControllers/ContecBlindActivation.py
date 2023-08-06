from enum import Enum
from .IControllerUnit import IControllerUnit
from .ActivationType import ActivationType
from .ContecActivation import ContecActivation

class BlindState(Enum):
    Stop = 0,
    MovingUp = 1,
    MovingDown = 2

class ContecBlindActivation(ContecActivation):

    def __init__(self, activationNumber: int, controllerUnit: IControllerUnit) -> None:
        super().__init__(activationNumber, controllerUnit, ActivationType.Blind)
        self.__BlindOpeningPercentage = 0
        self.__MovingDirection = BlindState.Stop
    
    @property
    def BlindOpeningPercentage(self) -> int:
        return self.__BlindOpeningPercentage
    
    @property
    def MovingDirection(self) -> BlindState:
        return self.__MovingDirection

    def SetNewState(self, movingDirection: BlindState, blindOpeningPercentage: int) -> None:
        if self.MovingDirection != movingDirection or self.BlindOpeningPercentage != blindOpeningPercentage:
            self.__MovingDirection = movingDirection
            self.__BlindOpeningPercentage = blindOpeningPercentage
            # StateChanged?.Invoke(MovingDirection, BlindOpeningPercentage);
        
        # SignalRefresh();

    def ParseStateRegisters(self, stateRegisters: list[int]) -> None:
        nextActivationNumber: int = self.StartActivationNumber + 1
        activationsPushersState, activationsOnOffState = stateRegisters[0].to_bytes(2, "big")
        #_upSwitch.SetPressStatus(IsByteOn(activationsPushersState, StartActivationNumber));
        #_downSwitch.SetPressStatus(IsByteOn(activationsPushersState, nextActivationNumber));
        additionalStateBytes: list[int] = stateRegisters[int(1 + (self.StartActivationNumber / 4))].to_bytes(2, "little") # if StartActivationNumber is in range 0-8, the indexes will be 1,1,1,1,2,2,2,2
        openingRatio: int = additionalStateBytes[int(int(self.StartActivationNumber / 2) % 2)] # if StartActivationNumber is in range 0-8, the indexes will be 0,0,1,1,0,0,1,1
        blindState: BlindState = BlindState.MovingUp if ContecActivation.IsByteOn(activationsOnOffState, self.StartActivationNumber) else BlindState.MovingDown if ContecActivation.IsByteOn(activationsOnOffState, nextActivationNumber) else BlindState.Stop
        self.SetNewState(blindState, openingRatio)
