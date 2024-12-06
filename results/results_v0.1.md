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

Participants answered the POMS questionnaire immediately before and after the MRI neurofeedback session. The results are shown in the following figure. The statistical comparison between the pre- and post- POMS scores was performed using a Wilcoxon signed-rank test (paired samples) with Holm-Bonferroni correction (p=0.05).

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

For the last three subjects, I saved the signal that was used to provide feedback during the sham runs - a random value from a uniform distribution between 0 and 1. The average values of the interhemispheric correlation that were used to create the feedback signal are shown in the following figure. The sham values are distributed around 0.5, which is the expected value for a random uniform distribution. Also, the statistical comparison between the active and sham feedback values was performed using an independent sample t-test and is highly significant.
```{figure} #fig-tbv-feedback-provided
:label: tbv-feedback-provided
Average values of interhemispheric correlation that were used to create the feedback signal.
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


Analyzing motor imagery and music responses together vs noise and rest conditions
```{figure} #fig-glm-group-loc-miplusmusic
:label: glm-group-nf-loc-miplusmusic
Group-level analysis of the localizer runs contrasting Motor Imagery and Music with Noise and Rest conditions.
```

| **Cluster ID** | **X** | **Y** | **Z** | **Peak Stat** | **Cluster Size (mm3)** | **AAL3**           | **Neurosynth**                |
|----------------|-------|-------|-------|---------------|------------------------|--------------------|-------------------------------|
| 1              | -51   | 12    | 6     | 6.972636152   | 29123                  | Frontal_Inf_Oper_L | Language                      |
| 1a             | -42   | 21    | 2     | 5.766479932   |                        | Frontal_Inf_Tri_L  | syntactic                     |
| 1b             | -51   | -6    | -2    | 5.538355863   |                        | Temporal_Sup_L     | auditory                      |
| 1c             | -51   | -21   | 6     | 5.177495118   |                        | Temporal_Sup_L     | auditory                      |
| 2              | 48    | 9     | -2    | 6.045763082   | 19786                  | Insula_R           | insula                        |
| 2a             | 60    | 15    | 26    | 5.756540689   |                        | Frontal_Inf_Oper_R | ventral premotor              |
| 2b             | 54    | 12    | 10    | 5.388923074   |                        | Frontal_Inf_Oper_R | motor                         |
| 2c             | 36    | 24    | -2    | 5.361725684   |                        | Insula_R           | anterior insula               |
| 3              | 0     | 6     | 62    | 5.4974644     | 35227                  | Supp_Motor_Area_L  | supplementary motor           |
| 3a             | -6    | 18    | 46    | 5.234865047   |                        | Supp_Motor_Area_L  | task, word                    |
| 3b             | -33   | -9    | 62    | 5.128314558   |                        | Precentral_L       | premotor                      |
| 3c             | 9     | 12    | 46    | 4.967065708   |                        | Supp_Motor_Area_R  | task, supplementary motor     |
| 4              | -36   | -45   | 42    | 5.032703571   | 11383                  | Parietal_Inf_L     | intraparietal sulcus          |
| 4a             | -51   | -45   | 66    | 4.602025774   |                        | Undefined          | ---                           |
| 4b             | -51   | -39   | 54    | 4.309947326   |                        | Parietal_Inf_L     | parietal, oddball             |
| 4c             | -51   | -33   | 38    | 4.174673914   |                        | Parietal_Inf_L     | anterior intraparietal, motor |
| 5              | 54    | -18   | 6     | 4.582884504   | 1903                   | Temporal_Sup_R     | auditory                      |
| 6              | 45    | -36   | 54    | 4.412989689   | 3231                   | Parietal_Inf_R     | intraparietal sulcus          |
| 6a             | 45    | -48   | 62    | 4.349033701   |                        | Parietal_Sup_R     | deficient, parietal           |
| 6b             | 36    | -33   | 42    | 4.268574105   |                        | Postcentral_R      | movements, premotor           |
| 7              | 54    | 51    | -6    | 4.38947044    | 395                    | Undefined          | ---                           |
| 8              | -45   | 42    | -2    | 4.278127958   | 897                    | Frontal_Inf_Tri_L  | semantic, linguistic          |
| 9              | 21    | -63   | -18   | 4.204419312   | 825                    | Cerebellum_6_R     | cerebellum, finger            |
| 10             | 30    | -9    | 70    | 4.021845009   | 1795                   | Frontal_Sup_2_R    | motor imagery                 |
| 10a            | 24    | -3    | 54    | 3.70449673    |                        | Frontal_Sup_2_R    | frontal eye fields            |
| 11             | -45   | 60    | 14    | 4.011386401   | 359                    | Undefined          | ---                           |
| 12             | -30   | -63   | -26   | 3.983957945   | 430                    | Cerebellum_6_L     | cerebellum                    |

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


