# musicnf-novelinterface
 
**A novel interface for rt-fMRI neurofeedback using music**

Here, we present and validate a musical interface for real-time fMRI neurofeedback, applicable in various experimental protocols. The interface is tested using a previously explored motor imagery connectivity-based functional paradigm. To establish both feasibility and utility, we compare the modulation of the bilateral premotor cortex (PMC) during functional runs with real versus sham (random) feedback. Additionally, we compare the musical feedback’s efficacy with a visual feedback interface.

Authors: Alexandre Sayal, João Pereira, Teresa Sousa, Bruno Direito, Miguel Castelo-Branco

CIBIT, University of Coimbra, Portugal

2024

## To Do List:
- [] Adicionar preditor para o boop
- [] Separar preditores 1a e 2a parte do bloco
- [] Distribuição do feedback durante o sham vs. real
- [] Usar ROIs real vs. sham para gerar TCs
- [] Sinal de feedback como preditor no glm
  - [] regiões que respondem à variação do feedback
  - [] derivada do preditor para codificar a valência do acorde (>0 - preditor positivo, <0 - preditor negativo)
- [] Estudo manuel para ROI putamen/amygdala
- [] Check for modulator subjects (subjects that activate vs. ones who do not)
  - [] Test Correlation of active vs. rest - criteria.
  - [] Apply the same rule to the visual feedback group
- [] Fetch stats from Learning network (putamen, dorsal striatum), monitoring
- [] Fetch stats from Reward network
- [] The role of the insula (cognitive control, conflicting - artigo Rebola 2012)
- [] Music vs. Noise (Localizer) vs. MI vs. Rest (NF) - contraste 2nd level