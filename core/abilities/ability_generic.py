from core.abilities.ability_base import Ability, AbilityCollection, register_ability
from core.rolls import Rolls
from core.rollable import Rollable, RollableWrapper
from core.abilities.ability_positions import Pos, BattlePhase


class GenericAbilities(AbilityCollection):
    pass


generic_abilities = GenericAbilities()


@register_ability(generic_abilities)
class LethalHits(Ability):
    def __init__(self):
        super().__init__(
            name=f"Lethal Hits",
            description="Does the things",
            position=Pos.HITS_APPLY_CRIT_EFFECTS,
        )

    def apply(self, hits: Rolls) -> Rolls:
        hits.successes -= hits.crits
        return hits

    def apply_special(self, hits: Rolls, wounds: Rolls) -> Rolls:
        wounds.successes += hits.crits
        return wounds


@register_ability(generic_abilities, modifier_list=[1, 2, "1d3"])
class SustainedHits(Ability):
    def __init__(self, modifier: Rollable | int | None = 1):
        super().__init__(
            name=f"Sustained Hits {modifier}",
            description="Performs additional hits",
            modifier=modifier,
            position=Pos.HITS_APPLY_CRIT_EFFECTS,
        )

    def apply(self, hits: Rolls) -> Rolls:
        modifier_value = int(self.modifier)
        hits.successes += modifier_value * hits.crits
        return hits
