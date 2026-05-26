# DataLoader Teaching Deck

Purpose: host live JupyterLab-first teaching decks that explain AICR
DataLoader benchmark findings.

Open the DataLoader deck in Binder with:

```text
urlpath=/lab/tree/apps/story/dataloader_ddp_story.ipynb
```

The notebook uses Jupyter slideshow metadata, `jupyterlab-rise`, Plotly
dropdowns, and bundled public DataLoader figures under
`assets/dataloader/figures`. The main story is DataLoader-first: the input
pipeline is a parallel queueing system, and the throughput heatmaps, imbalance
heatmaps, candidate frontiers, and scale plots show how tuning knobs affect
bottlenecks before DDP validates the training path.
