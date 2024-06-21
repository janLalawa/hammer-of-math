from utils import *
from core import *
from sim.sim import run_simulation, run_multiple_simulations_for_average
from core.units import allarus_custodians, ork_boyz, teq, meq, veq


def main():
    run_simulation()

    teq_sim = run_multiple_simulations_for_average(5000, Scenario([(allarus_custodians, 3)], (teq, 5)))

    ork_sim = run_multiple_simulations_for_average(5000, Scenario([(allarus_custodians, 3)], (ork_boyz, 30)))

    meq_sim = run_multiple_simulations_for_average(5000, Scenario([(allarus_custodians, 3)], (meq, 10)))

    veq_sim = run_multiple_simulations_for_average(5000, Scenario([(allarus_custodians, 3)], (veq, 1)))

    # Print stats breakdown

    print(f"Space Marines Damage: {meq_sim.total_damage_not_fnp / 5000}")
    print(f"Orks Damage: {ork_sim.total_damage_not_fnp / 5000}")
    print(f"Terminators Damage: {teq_sim.total_damage_not_fnp / 5000}")
    print(f"Vehicles Damage: {veq_sim.total_damage_not_fnp / 5000}")

    # attackers = allarus_custodians
    # defender = ork_boyz

    # my_game = Scenario(attackers, defender)
    #
    # print("------------pyHammer-------------")
    # print(
    #     "Wound Roll Needed: ",
    #     wound_roll_needed(
    #         my_game.attackers.weapon.strength, my_game.defender.toughness
    #     ),
    # )
    # print(
    #     "Save Roll Needed: ",
    #     save_roll_needed(
    #         my_game.attackers.weapon.ap, my_game.defender.save, my_game.defender.invuln
    #     ),
    # )
    # print("Attacks: ", my_game.attackers.weapon.attacks)
    # print("---------------------------------")
    #
    # print("-------------Hits-----------------")
    # hit_rolls = rollx(my_game.attackers.weapon.attacks)
    # print("Hit Rolls: ", hit_rolls)
    # hits = calculate_hits(hit_rolls, my_game.attackers.weapon.bs)
    # print("Hits: ", hits)
    # print("---------------------------------")
    #
    # print("-----------Reroll Hits-----------")
    # rerolled_hit_rolls = reroll_1s(hit_rolls)
    # print("Rerolled Hit Rolls: ", rerolled_hit_rolls)
    # rerolled_hits = calculate_hits(rerolled_hit_rolls, my_game.attackers.weapon.bs)
    # print("Rerolled Hits: ", rerolled_hits)
    # print("---------------------------------")
    #
    # print("----------Critical Hits----------")
    # lethal_hits = True
    # lethal_hits_count = 0
    # crit_count = calculate_crits(rerolled_hit_rolls, my_game.to_crit)
    # hits_with_sustained_rolls = append_crit_rolls_to_list(
    #     rerolled_hit_rolls, my_game.to_crit
    # )
    # sustained_hits_count = calculate_hits(
    #     hits_with_sustained_rolls, my_game.attackers.weapon.bs
    # )
    #
    # if lethal_hits:
    #     lethal_hits_count = crit_count
    #     sustained_hits_count -= crit_count
    #
    # print("Crit Count: ", crit_count)
    # print("Sustained Rolls: ", hits_with_sustained_rolls)
    # print(
    #     f"Hits With Crits: {sustained_hits_count} ({calc_percentage(sustained_hits_count, my_game.attackers.weapon.attacks)}%)"
    # )
    # print(f"Lethal Hits: {lethal_hits_count}")
    #
    # print("---------------------------------")
    #
    # print("-----------Roll Wounds-----------")
    # wound_rolls = rollx(sustained_hits_count)
    # wound_roll_needed_val = wound_roll_needed(
    #     my_game.attackers.weapon.strength, my_game.defender.toughness
    # )
    # wounds = calculate_wounds(wound_rolls, wound_roll_needed_val)
    # print("Wound Rolls: ", wound_rolls)
    # print(f"Wounds: {wounds} + {lethal_hits_count} Lethal Hits")
    # wounds += lethal_hits_count
    # print("---------------------------------")
    #
    # print("--------------Saves-------------")
    # save_rolls = rollx(wounds)
    # save_roll_needed_val = save_roll_needed(
    #     my_game.attackers.weapon.ap, my_game.defender.save, my_game.defender.invuln
    # )
    # saves = calculate_saves(save_rolls, save_roll_needed_val)
    # print("Save Rolls: ", save_rolls)
    # final_wounds = wounds - saves
    # print(f"Saves: {saves} ({calc_percentage(saves, wounds)}% of Wounds Saved)")
    # print(
    #     f"Final Wounds: {final_wounds} ({calc_percentage(final_wounds, my_game.attackers.weapon.attacks)}% of Attacks Through)"
    # )
    # print("---------------------------------")


if __name__ == "__main__":
    main()
