---
exports:
    - format: pdf
---
# Results v0.1
Last update: 2024-11-22 18:00

## Behavioral metrics

Reports performed during the localizer run regarding how pleasant/unpleasant each chord was to listen to. Participants rated each chord in a 5-level scale from unpleasant to pleasant. The results are shown in the following figure. The statistical comparison between pleasant and unpleasant chords was performed using a Mann-Whitney U test (two-sided, P_val:1.461e-17 U_stat=6.656e+03).

```{figure} #fig:behav-loc-report
:label: behav-loc-report
Participants' ratings of the pleasantness of each chord during the localizer run.
```

Participants answered the POMS questionnaire immediately before and after the MRI neurofeedback session. The results are shown in the following figure. The statistical comparison between the pre- and post- POMS scores was performed using a Wilcoxon signed-rank test (paired samples).

```{figure} #fig:behav-poms
:label: behav-poms
Participants' POMS scores before and after the MRI neurofeedback session.
```

## Real-time metrics from TurboBV

```{figure} #fig-tbv-correlation-timecourses
:label: tbv-correlation-timecourses
Correlation timecourses from TurboBV per participant.
```

```{figure} #fig-tbv-correlation-timecourses-average
:label: tbv-correlation-timecourses-average
Average correlation timecourses from TurboBV across participants.
```




## GLM analyses

### Example design matrix for the localizer task

Example design matrix, showing the regressors for motion, physiological signals, CSF, and WM.

```{figure} sub-01_task-loc_run-1_design-matrix.png
:label: design-matrix
Design matrix for the first run of the localizer task.
```

### Localizer

```{figure} #fig-glm-group-loc-mi
:label: glm-group-nf-loc-mi
Group-level analysis of the localizer runs contrasting Motor Imagery with Rest.
```

```{figure} #fig-glm-group-loc-music
:label: glm-group-nf-loc-music
Group-level analysis of the localizer runs contrasting Music with Noise.
```

### Active and Sham neurofeedback runs
```{figure} #fig-glm-group-nf-active
:label: glm-group-nf-active
Group-level analysis of the active neurofeedback runs.
```

```{figure} #fig-glm-group-nf-sham
:label: glm-group-nf-sham
Group-level analysis of the sham neurofeedback runs.
```

### Active and Sham neurofeedback runs - First part of the block
```{figure} #fig-glm-group-nf-active-mi1
:label: glm-group-nf-active-mi1
Group-level analysis of the active neurofeedback runs - First part of the block.
```

```{figure} #fig-glm-group-nf-sham-mi1
:label: glm-group-nf-sham-mi1
Group-level analysis of the sham neurofeedback runs - First part of the block.
```

### Active and Sham neurofeedback runs - Second part of the block
```{figure} #fig-glm-group-nf-active-mi2
:label: glm-group-nf-active-mi2
Group-level analysis of the active neurofeedback runs - Second part of the block.
```

```{figure} #fig-glm-group-nf-sham-mi2
:label: glm-group-nf-sham-mi2
Group-level analysis of the sham neurofeedback runs - Second part of the block.
```

### Active and Sham neurofeedback runs - Comparing first with second part of the block
```{figure} #fig-glm-group-nf-active-mi1vsmi2
:label: glm-group-nf-active-mi1vsmi2
Group-level analysis of the active neurofeedback runs comparing the first and second part of the block.
```

```{figure} #fig-glm-group-nf-sham-mi1vsmi2
:label: glm-group-nf-sham-mi1vsmi2
Group-level analysis of the sham neurofeedback runs comparing the first and second part of the block.
```


## Comparing Active and Sham neurofeedback GLM maps
Considered spatial smoothing of 8 mm FWHM. Paired analysis, 22 subjects.

### Whole-brain
```{figure} #fig-glm-design-activeVSsham
:label: glm-design-activeVSsham
Design matrix comparing the active and sham neurofeedback runs.
```

```{figure} #fig-glm-map-activeVSsham
:label: glm-map-activeVSsham
Whole-brain glm activation results comparing the active and sham neurofeedback runs.
```

```{table} Cluster-level results comparing the active and sham neurofeedback runs.
:label: glm-clusters-activeVSsham
![](#tab-glm-clusters-activeVSsham)
```

### Reward mask from Neurosynth

```{figure} #fig-neurosynth-reward-roi
:label: neurosynth-reward-roi
Reward mask from Neurosynth.
```

```{figure} #fig-glm-map-activeVSsham-reward-roi
:label: glm-map-activeVSsham-reward-roi
Glm activation results comparing the active and sham neurofeedback runs within the reward mask.
```

```{table} Cluster-level results comparing the active and sham neurofeedback runs within the reward mask.
:label: glm-clusters-activeVSsham-reward-roi
![](#tab-glm-clusters-activeVSsham-reward-roi)
```

## Comparing visual with music interface

22 music subjects vs. 10 visual subjects, spatial smoothing of 8 mm FWHM.

### Whole-brain

```{figure} #fig-musicVSvisual-glm-map
:label: musicVSvisual-glm-map
Glm activation results comparing the active music and visual interfaces.
```


```{table} Cluster-level results comparing the active music and visual interfaces.
:label: musicVSvisual-glm-clusters
![](#tab-musicVSvisual-glm-clusters)
```

## Comparing the first half with the second half of the neurofeedback runs

```{figure} #fig-glm-group-nf-onevstwo
:label: glm-group-nf-onevstwo
GLM activation results comparing the first and second half of the imagery runs (active NF).
```

