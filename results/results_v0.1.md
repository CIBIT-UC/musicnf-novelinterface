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

## GLM analysis

Example design matrix, showing the regressors for motion, physiological signals, CSF, and WM.

```{figure} sub-01_task-loc_run-1_design-matrix.png
:label: design-matrix
Design matrix for the first run of the localizer task.
```

```{figure} #fig-glm-group-nf-active
:label: glm-group-nf-active
Group-level analysis of the active neurofeedback runs.
```

```{figure} #fig-glm-group-nf-sham
:label: glm-group-nf-sham
Group-level analysis of the sham neurofeedback runs.
```

```{figure} #fig-glm-group-loc-mi
:label: glm-group-nf-loc-mi
Group-level analysis of the localizer runs contrasting Motor Imagery with Rest.
```

```{figure} #fig-glm-group-loc-music
:label: glm-group-nf-loc-music
Group-level analysis of the localizer runs contrasting Music with Noise.
```



