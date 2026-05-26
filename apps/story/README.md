# DataLoader Teaching Deck

Purpose: host live JupyterLab-first teaching decks that explain AICR
DataLoader benchmark findings.

Open the DataLoader deck in Binder with:

```text
urlpath=/lab/tree/apps/story/dataloader_ddp_story.ipynb
```

The notebook uses Jupyter slideshow metadata, `jupyterlab-rise`, and Plotly
dropdowns. The main story is DataLoader-first: it teaches where input work
lives, how tuning knobs affect bottlenecks, when backend choice changes, when
prepared inputs are useful, and why DDP is the training-validation handoff.
