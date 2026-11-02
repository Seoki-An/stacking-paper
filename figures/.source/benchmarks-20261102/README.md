# Benchmark figure sources (2026-11-02)

Editable PowerPoint: `benchmark-figures-latex.pptx`.

- Slide 1: seesaw trajectories, structure-wide equilibrium on the left and candidate-only equilibrium on the right.
- Slide 2: MCTS versus greedy wall construction. The two titles have been moved closer to the scenes, and the small numerical subtitles have been removed. Numbers remain in the paper caption. This is a single recorded example using seed 6 and the same 49-stone inventory; search times are not matched.
- Slide 3: initial pose sampling, with three independent IguanaTeX vector labels. These were regenerated using the installed `IguanaTex_v1_58.ppam!RegenerateSelectedDisplays` macro. The resulting native PowerPoint groups retain `LATEXADDIN` source and `BITMAPVECTOR=1`; use IguanaTeX's **Edit LaTeX display** to edit them.
- All panel titles use 24pt LaTeX with the same Times math/text setup on a 720pt-wide slide. The adjacent `.tex` and `.svg` files are retained. Slides 1 and 2 use outlined SVG labels with their TeX stored in alternative text.

The source data come from `../../../../figures/benchmarks` (the project-level figures directory). The new sampling figure comes from the project-level `figures/initial-pose-sampling/proposal_pipeline.pdf`. Original files outside the LaTeX project were left unchanged.

## Final figure assets

`../../pose_optimization_toy.eps`, `../../mcts_example.eps`, and `../../initial_pose_sampling.eps` were saved by Adobe Illustrator 30.8.2. The manuscript includes these EPS files using their generated `-eps-converted-to.pdf` companions. The plain `.pdf` files are Illustrator's corresponding PDF exports.

## Quality preservation

- PowerPoint reduced the seesaw image from 4800 x 1800 to 1999 x 749 pixels in its PDF export. `preserve_quality.py` restores the original pixels before Illustrator conversion.
- The MCTS scene retains the original PDF's vector geometry, with the old text removed and the outlined LaTeX labels from slide 2 merged at the same positions. This avoids depending on PowerPoint's conversion of the dense SVG scene.
- Sampling's embedded font for the hat accent was not preserved when opened directly in Illustrator. The original bottom titles are removed, then embedded fonts are converted to outlines with Ghostscript's `-dNoOutputFonts`, with image downsampling disabled. `initial_pose_sampling-revised-final.pdf` combines this original vector scene with the independent IguanaTeX labels from slide 3. Illustrator opens this final PDF.
- All EPS-to-PDF conversions disable color, grayscale, and monochrome image downsampling. Final figure and manuscript pages were inspected with PyMuPDF; the installed MiKTeX `pdftoppm` showed misleading speckling on vector paths.
- `tight_export.jsx` saves the revised MCTS and sampling EPS files using artboard 1 only, excluding artwork outside the intended crop. Its `*-tight-01.eps` outputs are copied to the canonical figure names. This prevents the original slide's unused lower region from returning as EPS whitespace.
- The optional binary TIFF-preview wrapper is removed from these two final EPS files for compatibility with MiKTeX's EPS parser. Their PostScript sections are copied unchanged, preserving all vector paths and image data. Final sizes are 720 x 239 pt (MCTS) and 720 x 272 pt (sampling).

The scripts record the authoring process and are run from the LaTeX project root. They use `.tmp/benchmark-figures-20261102` as a work directory. `prepare.py` and `make_ppt.py` create the initial deck; `revise_labels.py` performs the subsequent PowerPoint/IguanaTeX edits. `compose_revised.py` updates the MCTS layout, and `compose_sampling_fast.py` builds the final sampling composition without flattening the original scene. PowerPoint and Illustrator automation require their Windows applications. Original and composed PDFs are retained here.

Seesaw alignment check: the 4800 x 1800 source has two identical panel bounds. Within each 2400px-wide panel, artwork spans x=129 to x=2271, giving equal 129px left/right margins and an exact 1200px horizontal center. No horizontal shift was applied.

Compact seesaw revision: `compact_seesaw.py` reduces the scene to 80% (576 x 216 pt, centered on the 720 pt canvas) while preserving both vector labels at their original size. The labels move up to y=224 pt and align with the smaller panels. The final figure is 720 x 252 pt; `compact_seesaw_export.jsx` exports it through Illustrator. The original 4800 x 1800 pixels are retained. Slide 1 of the editable deck reflects this layout, and the manuscript caption is shortened.

The prior manuscript and sampling assets are backed up under `.backups/benchmark-figures-20261102` relative to the LaTeX root.
