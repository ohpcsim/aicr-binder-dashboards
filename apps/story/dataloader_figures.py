"""Public DataLoader figure inventory for the teaching deck."""

PUBLIC_REPO = "ohpcsim/aicr-public"
PUBLIC_COMMIT = "b3e610f486b42d1363dbb0f2591a315116564498"
FIGURE_PREFIX = "Cambridge/aicr-bench/docs/modules/dataloader/studies/figures"


def public_figure_url(name: str) -> str:
    """Return a pinned raw GitHub URL for a public DataLoader figure."""
    return (
        f"https://raw.githubusercontent.com/{PUBLIC_REPO}/{PUBLIC_COMMIT}/"
        f"{FIGURE_PREFIX}/{name}"
    )


FIGURE_GROUPS = [
    {
        "act": "Single-GPU Surface",
        "read": "The first surface shows the local throughput plateau before ranks enter the story.",
        "slides": [
            (
                "Single-GPU Throughput Surfaces",
                [
                    "dataloader-single-gpu-throughput-b200-2026-05-12.png",
                    "dataloader-single-gpu-throughput-rtxpro6000-2026-05-12.png",
                ],
            ),
        ],
    },
    {
        "act": "One-Node Replicated Rank Pressure",
        "read": "The one-node plots show how worker count, batch, and prefetch feed eight ranks; imbalance is the hidden cost.",
        "slides": [
            (
                "B200 One-Node Throughput And Imbalance",
                [
                    "dataloader-one-node-replicated-throughput-matrix-b200-2026-05-12.png",
                    "dataloader-one-node-replicated-imbalance-matrix-b200-2026-05-12.png",
                ],
            ),
            (
                "B200 One-Node Candidate Frontier",
                [
                    "dataloader-one-node-replicated-candidate-scatter-b200-2026-05-12.png",
                ],
            ),
            (
                "RTX One-Node Throughput And Imbalance",
                [
                    "dataloader-one-node-replicated-throughput-matrix-rtxpro6000-2026-05-12.png",
                    "dataloader-one-node-replicated-imbalance-matrix-rtxpro6000-2026-05-12.png",
                ],
            ),
            (
                "RTX One-Node Candidate Frontier",
                [
                    "dataloader-one-node-replicated-candidate-scatter-rtxpro6000-2026-05-12.png",
                ],
            ),
            (
                "RTX Batch/Prefetch Refinement Heatmaps",
                [
                    "dataloader-one-node-replicated-batch-prefetch-throughput-matrix-rtxpro6000-2026-05-12.png",
                    "dataloader-one-node-replicated-batch-prefetch-imbalance-matrix-rtxpro6000-2026-05-12.png",
                ],
            ),
            (
                "RTX Batch/Prefetch Candidate Frontier",
                [
                    "dataloader-one-node-replicated-batch-prefetch-candidate-scatter-rtxpro6000-2026-05-12.png",
                ],
            ),
        ],
    },
    {
        "act": "Multi-Node Parameter Selection",
        "read": "The multi-node plots show where a high-throughput local row becomes a distributed balance problem.",
        "slides": [
            (
                "B200 First-Stage Multi-Node Heatmaps",
                [
                    "dataloader-b200-multinode-first-stage-throughput-matrix-2026-05-13.png",
                    "dataloader-b200-multinode-first-stage-imbalance-matrix-2026-05-13.png",
                ],
            ),
            (
                "B200 Per-Node And Candidate Frontier",
                [
                    "dataloader-b200-multinode-first-stage-throughput-per-node-matrix-2026-05-13.png",
                    "dataloader-b200-multinode-followup-candidate-scatter-2026-05-13.png",
                ],
            ),
            (
                "B200 Multi-Node Samples Per Node",
                [
                    "dataloader-b200-multinode-samples-per-node-2026-05-13.png",
                ],
            ),
            (
                "RTX First-Stage Multi-Node Heatmaps",
                [
                    "dataloader-rtx-multinode-throughput-matrix-2026-05-12-13.png",
                    "dataloader-rtx-multinode-imbalance-matrix-2026-05-12-13.png",
                ],
            ),
            (
                "RTX Per-Node And Candidate Frontier",
                [
                    "dataloader-rtx-multinode-throughput-per-node-matrix-2026-05-12-13.png",
                    "dataloader-rtx-multinode-candidate-scatter-2026-05-12-13.png",
                ],
            ),
            (
                "RTX Follow-Up Multi-Node Heatmaps",
                [
                    "dataloader-rtx-multinode-imbalance-matrix-2026-05-13.png",
                    "dataloader-rtx-multinode-candidate-scatter-2026-05-13.png",
                ],
            ),
            (
                "RTX Multi-Node Samples Per Node",
                [
                    "dataloader-rtx-multinode-samples-per-node-2026-05-13.png",
                ],
            ),
        ],
    },
    {
        "act": "Scale Probe",
        "read": "Scale plots test whether the chosen balance survives more nodes.",
        "slides": [
            (
                "B200 8/16-Node Heatmaps",
                [
                    "dataloader-b200-8-16node-throughput-matrix-2026-05-14.png",
                    "dataloader-b200-8-16node-imbalance-matrix-2026-05-14.png",
                ],
            ),
            (
                "B200 2/4/8/16 Scale",
                [
                    "dataloader-b200-multinode-samples-per-node-2-4-8-16-2026-05-14.png",
                    "dataloader-b200-multinode-imbalance-2-4-8-16-2026-05-14.png",
                ],
            ),
            (
                "B200 Scale Candidate Frontier",
                [
                    "dataloader-b200-scale-probe-candidate-scatter-2026-05-14.png",
                ],
            ),
            (
                "RTX Eight-Node Heatmaps",
                [
                    "dataloader-rtx-8node-throughput-matrix-2026-05-13.png",
                    "dataloader-rtx-8node-imbalance-matrix-2026-05-13.png",
                ],
            ),
            (
                "RTX Eight-Node Candidate Frontier",
                [
                    "dataloader-rtx-8node-candidate-scatter-2026-05-13.png",
                ],
            ),
            (
                "RTX 2/4/8 Scale",
                [
                    "dataloader-rtx-multinode-samples-per-node-2-4-8-2026-05-13.png",
                    "dataloader-rtx-multinode-imbalance-2-4-8-2026-05-13.png",
                ],
            ),
        ],
    },
    {
        "act": "DALI And Backend Crossover",
        "read": "These plots show why representation and image size change whether DALI amortizes its pipeline overhead.",
        "slides": [
            (
                "DALI On Standard ImageNet",
                [
                    "dataloader-dali-standard-imagenet-b200-2026-05-20-top-configs.png",
                    "dataloader-dali-standard-imagenet-rtxpro6000-2026-05-20-top-configs.png",
                ],
            ),
            (
                "CPU 1024 JPEG Tuning",
                [
                    "dataloader-cpu-1024-optimization-b200-2026-05-20-top-configs.png",
                    "dataloader-cpu-1024-optimization-rtxpro6000-2026-05-20-top-configs.png",
                ],
            ),
            (
                "DALI 1024 JPEG Tuning",
                [
                    "dataloader-dali-1024-optimization-b200-2026-05-20-top-configs.png",
                    "dataloader-dali-1024-optimization-rtxpro6000-2026-05-20-top-configs.png",
                ],
            ),
            (
                "Optimized Backend Crossover",
                [
                    "dataloader-optimized-224-1024-backend-crossover-2026-05-20.png",
                    "dataloader-backend-dali-crossover-100x500-2026-05-23.png",
                ],
            ),
            (
                "Derived 224 Context",
                [
                    "dataloader-backend-dali-crossover-224-context-2026-05-24.png",
                ],
            ),
        ],
    },
    {
        "act": "Input Lab And Representation",
        "read": "Input-lab plots show how image size and representation change the mechanism, not just the winning backend.",
        "slides": [
            (
                "Input-Lab Throughput By Platform",
                [
                    "dataloader-input-lab-throughput-b200-2026-05-19.png",
                    "dataloader-input-lab-throughput-rtxpro6000-2026-05-19.png",
                ],
            ),
            (
                "Input-Lab Image Size Effect",
                [
                    "dataloader-input-lab-image-size-b200-2026-05-19.png",
                    "dataloader-input-lab-image-size-rtxpro6000-2026-05-19.png",
                ],
            ),
            (
                "Input-Lab Speedup Versus Original",
                [
                    "dataloader-input-lab-speedup-original-b200-2026-05-19.png",
                    "dataloader-input-lab-speedup-original-rtxpro6000-2026-05-19.png",
                ],
            ),
            (
                "Input-Lab Same-Size Speedup",
                [
                    "dataloader-input-lab-speedup-same-size-b200-2026-05-19.png",
                    "dataloader-input-lab-speedup-same-size-rtxpro6000-2026-05-19.png",
                ],
            ),
        ],
    },
    {
        "act": "Prepared-Input Ceilings",
        "read": "Prepared-input plots teach pay once offline versus pay every run online.",
        "slides": [
            (
                "Prepared-Input Throughput And Read Rate",
                [
                    "dataloader-prepared-input-finalist-throughput-2026-05-20.png",
                    "dataloader-prepared-input-finalist-read-rate-2026-05-20.png",
                ],
            ),
            (
                "Prepared fp16 Speedup",
                [
                    "dataloader-prepared-input-finalist-fp16-speedup-2026-05-20.png",
                ],
            ),
        ],
    },
]


FIGURE_FILENAMES = tuple(
    name
    for group in FIGURE_GROUPS
    for _, names in group["slides"]
    for name in names
)
