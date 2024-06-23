from core.scenario import Scenario
import plotly.graph_objects as go


def create_sankey_from_scenario(sankey_sim: Scenario):
    node_colors = [
        "red",  # Attacks
        "green",  # Hit
        "red",  # Missed
        "green",  # Wounded
        "red",  # Not Wounded
        "green",  # Unsaved
        "red",  # Saved
        "green",  # Total Hits Through
        "red",  # Total Failures
        "white",  # Invisible node to add padding
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=30,
            line=dict(color="black", width=0.5),
            label=[
                "Attacks",
                "Hit",
                "Missed",
                "Wounded",
                "Not Wounded",
                "Unsaved",
                "Saved",
                "Total Hits Through",
                "Total Failures",
                "",  # Invisible node
            ],
            color=node_colors
        ),
        link=dict(
            source=[
                0, 0,
                1, 1,
                3, 3,
                5,
                2, 4, 6,
                8, 8, 8  # Additional links to the invisible node
            ],
            target=[
                1, 2,
                3, 4,
                5, 6,
                7,
                8, 8, 8,
                9, 9, 9  # Invisible node
            ],
            value=[
                sankey_sim.average_hits, (sankey_sim.average_attacks - sankey_sim.average_hits),
                sankey_sim.average_wounds, (sankey_sim.average_hits - sankey_sim.average_wounds),
                sankey_sim.average_unsaved_saves, (sankey_sim.average_wounds - sankey_sim.average_unsaved_saves),
                sankey_sim.average_unsaved_saves,
                (sankey_sim.average_attacks - sankey_sim.average_hits),
                (sankey_sim.average_hits - sankey_sim.average_wounds),
                (sankey_sim.average_wounds - sankey_sim.average_unsaved_saves),
                0, 0, 0  # Zero values for the invisible node
            ],
            color=['rgba(0, 100, 0, 0.8)' if value > 0 else 'rgba(255, 0, 0, 0.8)' for value in [
                sankey_sim.average_hits, (sankey_sim.average_attacks - sankey_sim.average_hits),
                sankey_sim.average_wounds, (sankey_sim.average_hits - sankey_sim.average_wounds),
                sankey_sim.average_unsaved_saves, (sankey_sim.average_wounds - sankey_sim.average_unsaved_saves),
                sankey_sim.average_unsaved_saves,
                (sankey_sim.average_attacks - sankey_sim.average_hits),
                (sankey_sim.average_hits - sankey_sim.average_wounds),
                (sankey_sim.average_wounds - sankey_sim.average_unsaved_saves),
                0, 0, 0  # Invisible links
            ]]
        ))])

    fig.update_layout(title_text="40k Simulation", font_size=10)
    fig.show()
