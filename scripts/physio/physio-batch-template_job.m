%-----------------------------------------------------------------------
% Job saved on 15-Nov-2024 15:37:22 by cfg_util (rev $Rev: 8183 $)
% spm SPM - SPM25 (00.00)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.tools.physio.save_dir = {'/Volumes/T7/BIDS-MUSICNF/derivatives/physio-out/sub-02'};
matlabbatch{1}.spm.tools.physio.log_files.vendor = 'Siemens';
matlabbatch{1}.spm.tools.physio.log_files.cardiac = {'/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/sub-02/sub-02_task-loc_run-1.puls'};
matlabbatch{1}.spm.tools.physio.log_files.respiration = {'/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/sub-02/sub-02_task-loc_run-1.resp'};
matlabbatch{1}.spm.tools.physio.log_files.scan_timing = {'/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/sub-02/sub-02_task-loc_run-1_firstvol.dcm'};
matlabbatch{1}.spm.tools.physio.log_files.sampling_interval = [];
matlabbatch{1}.spm.tools.physio.log_files.relative_start_acquisition = [];
matlabbatch{1}.spm.tools.physio.log_files.align_scan = 'first';
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.Nslices = 26;
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.NslicesPerBeat = [];
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.TR = 1.5;
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.Ndummies = 0;
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.Nscans = 336;
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.onset_slice = 1;
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.time_slice_to_slice = [];
matlabbatch{1}.spm.tools.physio.scan_timing.sqpar.Nprep = [];
matlabbatch{1}.spm.tools.physio.scan_timing.sync.nominal = struct([]);
matlabbatch{1}.spm.tools.physio.preproc.cardiac.modality = 'PPU';
matlabbatch{1}.spm.tools.physio.preproc.cardiac.filter.no = struct([]);
matlabbatch{1}.spm.tools.physio.preproc.cardiac.initial_cpulse_select.auto_matched.min = 0.4;
matlabbatch{1}.spm.tools.physio.preproc.cardiac.initial_cpulse_select.auto_matched.file = 'initial_cpulse_kRpeakfile.mat';
matlabbatch{1}.spm.tools.physio.preproc.cardiac.initial_cpulse_select.auto_matched.max_heart_rate_bpm = 90;
matlabbatch{1}.spm.tools.physio.preproc.cardiac.posthoc_cpulse_select.off = struct([]);
matlabbatch{1}.spm.tools.physio.preproc.respiratory.filter.passband = [0.01 2];
matlabbatch{1}.spm.tools.physio.preproc.respiratory.despike = false;
matlabbatch{1}.spm.tools.physio.model.output_multiple_regressors = 'sub-02_task-loc_run-1_desc-physioregressors.txt';
matlabbatch{1}.spm.tools.physio.model.output_physio = 'sub-02_task-loc_run-1_desc-physioregressors.mat';
matlabbatch{1}.spm.tools.physio.model.orthogonalise = 'none';
matlabbatch{1}.spm.tools.physio.model.censor_unreliable_recording_intervals = false;
matlabbatch{1}.spm.tools.physio.model.retroicor.yes.order.c = 3;
matlabbatch{1}.spm.tools.physio.model.retroicor.yes.order.r = 4;
matlabbatch{1}.spm.tools.physio.model.retroicor.yes.order.cr = 1;
matlabbatch{1}.spm.tools.physio.model.rvt.yes.method = 'hilbert';
matlabbatch{1}.spm.tools.physio.model.rvt.yes.delays = 0;
matlabbatch{1}.spm.tools.physio.model.hrv.yes.delays = 0;
matlabbatch{1}.spm.tools.physio.model.noise_rois.no = struct([]);
matlabbatch{1}.spm.tools.physio.model.movement.no = struct([]);
matlabbatch{1}.spm.tools.physio.model.other.no = struct([]);
matlabbatch{1}.spm.tools.physio.verbose.level = 2;
matlabbatch{1}.spm.tools.physio.verbose.fig_output_file = '';
matlabbatch{1}.spm.tools.physio.verbose.use_tabs = false;
