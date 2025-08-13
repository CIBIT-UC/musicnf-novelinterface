clear, clc;

outputFolder = fullfile(pwd,'prt');

%% PRT Parameters
PRTParameters = struct();

PRTParameters.FileVersion = 2;
PRTParameters.Resolution = 'Volumes';
PRTParameters.ExperimentName = 'MusicNF_Main';
PRTParameters.BackgroundColor = [0 0 0];
PRTParameters.TextColor = [255 255 255];
PRTParameters.TimeCourseColor = [1 1 1];
PRTParameters.TimeCourseThick = 3;
PRTParameters.ReferenceFuncColor = [0 0 80];
PRTParameters.ReferenceFuncThick = 2;

%% PRT Conditions
condNames = {'Rest','MotorImagery','RestFinal'};

blockDuration = [ 20 20 8 ]; %in volumes (think TR = 1500ms)

blockColor = [216 83 25 ; 236 177 32 ; 110 115 190];

PRTParameters.nCond = length(condNames);

PRTConditions = struct();

for c = 1:PRTParameters.nCond
    
    PRTConditions.(condNames{c}).Color = blockColor(c,:);
    PRTConditions.(condNames{c}).BlockDuration = blockDuration(c);
    PRTConditions.(condNames{c}).Intervals = [];
    PRTConditions.(condNames{c}).NumBlocks = 0;
    
end

%% Run MRI D12 R2
SEQ = [   1 2 1 2 1 2 1 2 1 2 1 2 3];

[ PRTConditions_R2 ] = buildIntervals( SEQ , PRTConditions );

generatePRT( PRTParameters , PRTConditions_R2 , 'MusicNF_Main_v0.3_PostDiscard' , outputFolder );
