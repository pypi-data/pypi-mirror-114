from .OsuStrainSkill import OsuStrainSkill
from ..Objects.osu.HitObjects.DifficultyHitObject import DifficultyHitObject
from math import pi, sqrt, sin

class Aim(OsuStrainSkill):
    angle_bonus_begin = pi / 3
    timing_threshold = 107

    def __init__(self):
        super().__init__()
        self.SkillMultiplier = 26.25
        self.StrainDecayBase = 0.15

    def strainValueOf(self, currentObject):
        result = 0
        scale = 90

        def applyDimishingExp(val):
            return pow(val, 0.99)

        if(len(self.Previous) > 0):
            if(currentObject.Angle is not None and currentObject.Angle > 0 and currentObject.Angle > self.angle_bonus_begin):
                angleBonus = sqrt(
                    max(self.Previous[0].JumpDistance - scale, 0) *
                    pow(sin(currentObject.Angle - self.angle_bonus_begin), 2) *
                    max(currentObject.JumpDistance - scale, 0)
                )
                result = 1.4 * applyDimishingExp(max(0, angleBonus)) / max(self.timing_threshold, self.Previous[0].StrainTime)
        
        jumpDistanceExp = applyDimishingExp(currentObject.JumpDistance)
        travelDistanceExp = applyDimishingExp(currentObject.TravelDistance)

        returnValue = max(
            result + (jumpDistanceExp + travelDistanceExp + sqrt(travelDistanceExp * jumpDistanceExp)) / max(currentObject.StrainTime, self.timing_threshold),
            (sqrt(travelDistanceExp * jumpDistanceExp) + jumpDistanceExp + travelDistanceExp) / currentObject.StrainTime
        )

        return returnValue

