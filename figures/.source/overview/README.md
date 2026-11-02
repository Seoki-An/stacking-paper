# Overview source and export (2026-11-02)

`source.pptx` is the updated editable copy of the live project-level `figures/overview.pptx`. The live deck was saved as well. The user's previously unsaved state-image change is preserved; `before-update-20261102.pptx` records the exact pre-edit slide.

- Inventory uses the top three rows of the supplied 2400 x 2400 PNG, cropped to 2400 x 1800 without resampling. The original and crop are retained here.
- The state image is uniformly reduced to 90% of its previous displayed size. Its original image content and aspect ratio remain intact.
- The result label is now one line: `Selected action a_k^*`. It is an outlined LaTeX SVG, with its source saved alongside it and in the PPT shape metadata.
- Label font sizes are preserved. The state panel and lower arrows are repositioned rather than stretching the diagram. Final crop is 581 x 149 pt, versus the previous 581 x 161 pt (7.45% lower).

Later alignment revision: the selected-action box now sits below the backpropagation panel, aligned to its right edge and connected by a downward arrow. The right-hand excess is removed: current crop is **525 x 149 pt**. The manuscript inclusion width changes from 0.94 to 0.85 times text width to preserve the displayed text and node sizes; the main panels therefore move right within the centered figure. `../adjust_overview_and_masks_20261102.py` records this edit, and `../export_adjusted_20261102.jsx` exports the current figures.

Arrow refinement: selected-action box top is 168 pt and height is 11 pt. Its text size is unchanged and vertically centered. The downward arrow spans y=157.25 to 168 (10.75 pt), with a short, narrow triangular head, so its shaft remains visible. The overall crop and manuscript figure height remain unchanged.

`update_20261102.py` records the initial layout edit. The final deck additionally has the corrected standalone LaTeX SVG label and explicit lower line segments (filled arrowheads). Use `source.pptx` as the authoritative editable layout.

To export, save the slide as a full-slide PDF to `.tmp/overview-20261102/updated-full.pdf`, then run `restore_updated_images.py` from the LaTeX project root. PowerPoint downsamples and sometimes aliases small node-label images, so this script restores each individual image occurrence from the original PPT pixels and alpha mask; repeated PDF resources are split. The resulting `updated-20261102.pdf` retains the state image at 905 x 634 pixels and inventory at 2400 x 1800 pixels.

`export_updated.jsx` exports through Illustrator with image downsampling disabled. Strip the optional binary preview wrapper from the EPS and run epstopdf without image downsampling. Use that converted PDF as both `../../overview-eps-converted-to.pdf` and `../../overview.pdf`: Illustrator's direct PDF export made some transparent labels faint, whereas the EPS conversion preserves their contrast. The raw Illustrator PDF is retained as `illustrator-export-20261102.pdf` for provenance. Both the final EPS and manuscript were visually checked.
