import json
from pathlib import Path

from apps.story.dataloader_figures import FIGURE_FILENAMES, PUBLIC_COMMIT


DECK = Path("apps/story/dataloader_ddp_story.ipynb")


def load_deck():
    return json.loads(DECK.read_text(encoding="utf-8"))


def deck_text():
    data = load_deck()
    return "\n".join(
        "".join(cell.get("source", [])) for cell in data.get("cells", [])
    )


def test_story_deck_exists_and_has_slides():
    data = load_deck()
    cells = data.get("cells", [])
    slide_types = [
        cell.get("metadata", {}).get("slideshow", {}).get("slide_type")
        for cell in cells
    ]

    assert len(cells) >= 60
    assert slide_types.count("slide") >= 55
    assert "rise" in data.get("metadata", {})


def test_story_deck_scope_and_guardrails():
    text = deck_text()

    required = [
        "parallel queueing system",
        "Heatmaps Are The Story",
        "throughput heatmaps show the plateau",
        "imbalance heatmaps show the hidden distributed cost",
        "candidate scatter plots show the frontier",
        "Normal DALI JPEG Is Not GDS",
        "canonical-224",
        "derived-jpeg-1024",
        "DataLoader-only throughput selects candidates",
        "Synthetic GPU input removes the real input path",
        "Do not say DALI always wins",
        "Do not say DataLoader-only wins are training wins",
        "Do not recommend prepared fp16 as a general recipe",
        "Do not claim the normal DALI JPEG path uses GDS",
    ]
    for phrase in required:
        assert phrase in text

    excluded = ["HPL-MxP", "HPCG", "NCCL"]
    for phrase in excluded:
        assert phrase not in text


def test_story_deck_has_interactive_backbone():
    text = deck_text()

    required_functions = [
        "pipeline_sankey",
        "worker_scan_fig",
        "backend_crossover_fig",
        "prepared_economics_fig",
        "ddp_truth_fig",
        "input_ceiling_fig",
    ]
    for function_name in required_functions:
        assert function_name in text

    assert text.count("updatemenus") >= 5


def test_story_deck_includes_all_public_dataloader_figures():
    text = deck_text()

    assert len(FIGURE_FILENAMES) == 53
    assert PUBLIC_COMMIT in text

    for filename in FIGURE_FILENAMES:
        assert filename in text

    required_families = [
        "throughput-matrix",
        "imbalance-matrix",
        "candidate-scatter",
        "samples-per-node",
        "backend-dali-crossover",
        "prepared-input-finalist",
    ]
    for family in required_families:
        assert any(family in filename for filename in FIGURE_FILENAMES)
        assert family in text
