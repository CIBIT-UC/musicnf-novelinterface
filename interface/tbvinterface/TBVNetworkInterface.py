import time
import struct
import numpy as np
from TBVClient import TBVClient

class TBVNetworkInterface:
    def __init__(self, tbv_client):
        self.tbv_client = tbv_client

    def create_connection(self):
        self.tbv_client.create_connection()

    def close_connection(self):
        self.tbv_client.close_connection()

    def get_current_time_point(self):
        """
        Send: tGetCurrentTimePoint
        Receive: int CurrentTimePoint
        Provides the number of the currently processed step during real-time processing as an
        integer. Note that this function is 1-based, i.e. when the first step is processed the function
        returns "1" not "0"; this is important when the return value is used to access time-related
        information; in this case subtract "1" from the returned value.
        """
        rOK, aOK, message = self.tbv_client.query('tGetCurrentTimePoint')
        if rOK and aOK:
            current_time_point = int.from_bytes(message, byteorder="big")
        else:
            current_time_point = -1
        return current_time_point

    @staticmethod
    def byte_to_float(bytes):
        # Ensure bytes is a bytearray or bytes object with length 4
        if len(bytes) != 4:
            raise ValueError("Input must be a 4-byte array")
        
        # Reverse the byte order to match MATLAB's behavior (bytes(4:-1:1))
        reversed_bytes = bytes[::-1]
        
        # Convert bytes to float
        result = struct.unpack('f', reversed_bytes)[0]
        
        return result

    def get_project_name(self):
        """
        Send: tGetProjectName
        Receive: char ProjectName[256]
        Provides the name of the currently loaded project.
        """
        rOK, aOK, message = self.tbv_client.query('tGetProjectName')
        if rOK and aOK:
            # message size is the first four bytes
            message_size = int.from_bytes(message[:4], byteorder="big")
            # the project name is the rest of the message
            project_name = message[4:4 + message_size].decode('utf-8')
        else:
            project_name = ''
        return project_name
    
    def get_expected_nr_of_time_points(self):
        """
        Send: tGetExpectedNrOfTimePoints
        Receive: int ExpectedNrOfTimePoints
        Provides the expected number of time points for the currently loaded project.
        """
        rOK, aOK, message = self.tbv_client.query('tGetExpectedNrOfTimePoints')
        if rOK and aOK:
            expected_nr_of_time_points = int.from_bytes(message, byteorder="big")
        else:
            expected_nr_of_time_points = -1
        return expected_nr_of_time_points
    
    def get_dims_of_functional_data(self):
        """
        Send: tGetDimsOfFunctionalData
        Receive: int DimX, int DimY, int DimZ
        Provides the dimensions of the functional data.
        """
        rOK, aOK, message = self.tbv_client.query('tGetDimsOfFunctionalData')
        if rOK and aOK:
            # dim_x is encoded in the first 4 bytes, dim_y in the next 4 bytes, and dim_z in the last 4 bytes
            dim_x = int.from_bytes(message[:4], byteorder="big")
            dim_y = int.from_bytes(message[4:8], byteorder="big")
            dim_z = int.from_bytes(message[8:], byteorder="big")
        else:
            dim_x, dim_y, dim_z = -1, -1, -1
        return dim_x, dim_y, dim_z
    
    def get_project_name(self):
        """
        Send: tGetProjectName
        Receive: char ProjectName[256]
        Provides the name of the currently loaded project.
        """
        rOK, aOK, message = self.tbv_client.query('tGetProjectName')
        if rOK and aOK:
            # message size is the first four bytes
            message_size = int.from_bytes(message[:4], byteorder="big")
            # the project name is the rest of the message
            project_name = message[4:4 + message_size].decode('utf-8')
        else:
            project_name = ''
        return project_name
    
    def get_watch_folder(self):
        """
        Send: tGetWatchFolder
        Receive: char WatchFolder[256]
        Provides the watch folder.
        """
        rOK, aOK, message = self.tbv_client.query('tGetWatchFolder')
        if rOK and aOK:
            # message size is the first four bytes
            message_size = int.from_bytes(message[:4], byteorder="big")
            # the watch folder is the rest of the message
            watch_folder = message[4:4 + message_size].decode('utf-8')
        else:
            watch_folder = ''
        return watch_folder
    
    def get_target_folder(self):
        """
        Send: tGetTargetFolder
        Receive: char TargetFolder[256]
        Provides the target folder.
        """
        rOK, aOK, message = self.tbv_client.query('tGetTargetFolder')
        if rOK and aOK:
            # message size is the first four bytes
            message_size = int.from_bytes(message[:4], byteorder="big")
            # the target folder is the rest of the message
            target_folder = message[4:4 + message_size].decode('utf-8')
        else:
            target_folder = ''
        return target_folder
    
    def get_feedback_folder(self):
        """
        Send: tGetFeedbackFolder
        Receive: char FeedbackFolder[256]
        Provides the feedback folder.
        """
        rOK, aOK, message = self.tbv_client.query('tGetFeedbackFolder')
        if rOK and aOK:
            # message size is the first four bytes
            message_size = int.from_bytes(message[:4], byteorder="big")
            # the feedback folder is the rest of the message
            feedback_folder = message[4:4 + message_size].decode('utf-8')
        else:
            feedback_folder = ''
        return feedback_folder
    
    def get_current_protocol_condition(self):
        """
        Send: tGetCurrentProtocolCondition
        Receive: int CurrentProtocolCondition (zero-indexed)
        Provides the current protocol condition.
        """
        rOK, aOK, message = self.tbv_client.query('tGetCurrentProtocolCondition')
        if rOK and aOK:
            current_protocol_condition = int.from_bytes(message, byteorder="big")
        else:
            current_protocol_condition = ''
        return current_protocol_condition

    def get_full_nr_of_predictors(self):
        """
        Send: tGetFullNrOfPredictors
        Receive: int FullNrOfPredictors
        Provides the full number of predictors.
        """
        rOK, aOK, message = self.tbv_client.query('tGetFullNrOfPredictors')
        if rOK and aOK:
            full_nr_of_predictors = int.from_bytes(message, byteorder="big")
        else:
            full_nr_of_predictors = -1
        return full_nr_of_predictors
    
    def get_current_nr_of_predictors(self):
        """
        Send: tGetCurrentNrOfPredictors
        Receive: int CurrentNrOfPredictors
        Provides the current number of predictors.
        """
        rOK, aOK, message = self.tbv_client.query('tGetCurrentNrOfPredictors')
        if rOK and aOK:
            current_nr_of_predictors = int.from_bytes(message, byteorder="big")
        else:
            current_nr_of_predictors = -1
        return current_nr_of_predictors
    
    def get_nr_of_confound_predictors(self):
        """
        Send: tGetNrOfConfoundPredictors
        Receive: int NrOfConfoundPredictors
        Provides the number of confound predictors.
        """
        rOK, aOK, message = self.tbv_client.query('tGetNrOfConfoundPredictors')
        if rOK and aOK:
            nr_of_confound_predictors = int.from_bytes(message, byteorder="big")
        else:
            nr_of_confound_predictors = -1
        return nr_of_confound_predictors
    
    def get_value_of_design_matrix(self, pred, timepoint):
        """
        Send: tGetValueOfDesignMatrix
        Receive: int pred, int timepoint, float ValueOfDesignMatrix
        Provides the value of the design matrix.
        """
        rOK, aOK, message = self.tbv_client.query('tGetValueOfDesignMatrix', [pred, timepoint])
        if rOK and aOK:
            pred = int.from_bytes(message[:4], byteorder="big")
            timepoint = int.from_bytes(message[4:8], byteorder="big")
            value_of_design_matrix = struct.unpack('f', message[8:])[0]
        else:
            pred = -1
            timepoint = -1
            value_of_design_matrix = -1
        return pred, timepoint, value_of_design_matrix
    
    def get_nr_of_contrasts(self):
        """
        Send: tGetNrOfContrasts
        Receive: int NrOfContrasts
        Provides the number of contrasts.
        """
        rOK, aOK, message = self.tbv_client.query('tGetNrOfContrasts')
        if rOK and aOK:
            nr_of_contrasts = int.from_bytes(message, byteorder="big")
        else:
            nr_of_contrasts = -1
        return nr_of_contrasts

    def get_nr_of_rois(self):
        """
        Send: tGetNrOfROIs
        Receive: int NrOfROIs
        Provides the number of ROIs.
        """
        rOK, aOK, message = self.tbv_client.query('tGetNrOfROIs')
        if rOK and aOK:
            nr_of_rois = int.from_bytes(message, byteorder="big")
        else:
            nr_of_rois = -1
        return nr_of_rois

    def get_mean_of_roi(self, roi):
        """
        Send: tGetMeanOfROI
        Receive: int ROI, float MeanOfROI
        Provides the mean of the ROI.
        """
        rOK, aOK, message = self.tbv_client.query('tGetMeanOfROI', [roi])
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            mean_of_roi = self.byte_to_float(message[4:8])
        else:
            roi = -1
            mean_of_roi = -1
        return roi, mean_of_roi
    
    def get_mean_of_roi_at_time_point(self, roi, timepoint):
        """
        Send: tGetMeanOfROIAtTimePoint
        Receive: int ROI, int TimePoint, float MeanOfROIAtTimePoint
        Provides the mean of the ROI at the time point.
        """
        rOK, aOK, message = self.tbv_client.query('tGetMeanOfROIAtTimePoint', [roi, timepoint])

        # if the length of the message is not 12 bytes, then the message is not valid,\
        # aka, the ROI is out of range
        if len(message) != 12:
            rOK = False
            aOK = False
            print('!!!! --- ROI out of range')
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            timepoint = int.from_bytes(message[4:8], byteorder="big")
            mean_of_roi_at_time_point = self.byte_to_float(message[8:12])
        else:
            roi = -1
            timepoint = -1
            mean_of_roi_at_time_point = -1
        return roi, timepoint, mean_of_roi_at_time_point
    
    def get_nr_of_voxels_of_roi(self, roi):
        """
        Send: tGetNrOfVoxelsOfROI
        Receive: int ROI, int NrOfVoxelsOfROI
        Provides the number of voxels of the ROI.
        """
        rOK, aOK, message = self.tbv_client.query('tGetNrOfVoxelsOfROI', [roi])
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            nr_of_voxels_of_roi = int.from_bytes(message[4:], byteorder="big")
        else:
            roi = -1
            nr_of_voxels_of_roi = -1
        return roi, nr_of_voxels_of_roi
    
    def get_beta_of_roi(self, roi, pred):
        """
        Send: tGetBetaOfROI
        Receive: int ROI, int Pred, float BetaOfROI
        Provides the beta of the ROI.
        """
        rOK, aOK, message = self.tbv_client.query('tGetBetaOfROI', [roi, pred])
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            pred = int.from_bytes(message[4:8], byteorder="big")
            beta_of_roi = self.byte_to_float(message[8:12])
        else:
            roi = -1
            pred = -1
            beta_of_roi = -1
        return roi, pred, beta_of_roi
    
    def get_coords_of_voxel_of_roi(self, roi, voxel):
        """
        Send: tGetCoordsOfVoxelOfROI
        Receive: int ROI, int Voxel, int X, int Y, int Z
        Provides the coordinates of the voxel of the ROI.
        """
        rOK, aOK, message = self.tbv_client.query('tGetCoordsOfVoxelOfROI', [roi, voxel])
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            voxel = int.from_bytes(message[4:8], byteorder="big")
            x = int.from_bytes(message[8:12], byteorder="big")
            y = int.from_bytes(message[12:16], byteorder="big")
            z = int.from_bytes(message[16:], byteorder="big")
        else:
            roi = -1
            voxel = -1
            x = -1
            y = -1
            z = -1
        return roi, voxel, x, y, z
    
    def get_all_coords_of_voxels_of_roi(self, roi):
        """
        Send: tGetAllCoordsOfVoxelsOfROI
        Receive: int ROI, int NrOfVoxelsOfROI, int X, int Y, int Z
        Provides the coordinates of all voxels of the ROI.
        """
        rOK, aOK, message = self.tbv_client.query('tGetAllCoordsOfVoxelsOfROI', [roi])
        if rOK and aOK:
            roi = int.from_bytes(message[:4], byteorder="big")
            nr_of_voxels = len(message[4:]) / 3

            coords = np.zeros((nr_of_voxels, 3), dtype=int)
            for i in range(nr_of_voxels):
                x = int.from_bytes(message[4 + 3*i:4 + 3*i + 1], byteorder="big")
                y = int.from_bytes(message[4 + 3*i + 1:4 + 3*i + 2], byteorder="big")
                z = int.from_bytes(message[4 + 3*i + 2:4 + 3*i + 3], byteorder="big")
                coords[i, :] = [x, y, z]
        else:
            roi = -1
            nr_of_voxels = -1
            coords = []
        return roi, nr_of_voxels, coords
    
    def get_value_of_voxel_at_time_point(self, x, y, z, timepoint):
        """
        Send: tGetValueOfVoxelAtTimePoint
        Receive: int X, int Y, int Z, int TimePoint, float ValueOfVoxelAtTimePoint
        Provides the value of the voxel at the time point.
        """
        rOK, aOK, message = self.tbv_client.query('tGetValueOfVoxelAtTimePoint', [x, y, z, timepoint])
        if rOK and aOK:
            x = int.from_bytes(message[:4], byteorder="big")
            y = int.from_bytes(message[4:8], byteorder="big")
            z = int.from_bytes(message[8:12], byteorder="big")
            timepoint = int.from_bytes(message[12:16], byteorder="big")
            value_of_voxel_at_time_point = self.byte_to_float(message[16:20])
        else:
            x = -1
            y = -1
            z = -1
            timepoint = -1
            value_of_voxel_at_time_point = -1
        return x, y, z, timepoint, value_of_voxel_at_time_point
    
    def get_beta_of_voxel(self, x, y, z, pred):
        """
        Send: tGetBetaOfVoxel
        Receive: int X, int Y, int Z, int Pred, float BetaOfVoxel
        Provides the beta of the voxel.
        """
        rOK, aOK, message = self.tbv_client.query('tGetBetaOfVoxel', [pred, x, y, z])
        if rOK and aOK:
            pred = int.from_bytes(message[:4], byteorder="big")
            x = int.from_bytes(message[4:8], byteorder="big")
            y = int.from_bytes(message[8:12], byteorder="big")
            z = int.from_bytes(message[12:16], byteorder="big")
            beta_of_voxel = self.byte_to_float(message[16:20])
        else:
            x = -1
            y = -1
            z = -1
            pred = -1
            beta_of_voxel = -1
        return x, y, z, pred, beta_of_voxel
    
    def get_map_value_of_voxel(self, contrast, x, y, z):
        """
        Send: tGetMapValueOfVoxel
        Receive: int Contrast, int X, int Y, int Z, float MapValueOfVoxel
        Provides the map value of the voxel.
        """
        rOK, aOK, message = self.tbv_client.query('tGetMapValueOfVoxel', [contrast, x, y, z])
        if rOK and aOK:
            contrast = int.from_bytes(message[:4], byteorder="big")
            x = int.from_bytes(message[4:8], byteorder="big")
            y = int.from_bytes(message[8:12], byteorder="big")
            z = int.from_bytes(message[12:16], byteorder="big")
            map_value_of_voxel = self.byte_to_float(message[16:20])
        else:
            contrast = -1
            x = -1
            y = -1
            z = -1
            map_value_of_voxel = -1
        return contrast, x, y, z, map_value_of_voxel
    
    def get_pearson_correlation(self, window_size):
        """
        Send: tGetPearsonCorrelation
        Receive: int WindowSize, float PearsonCorrelation
        Provides the Pearson correlation.
        """
        rOK, aOK, message = self.tbv_client.query('tGetPearsonCorrelation', [window_size])
        if rOK and aOK:
            window_size = int.from_bytes(message[:4], byteorder="big")
            # each correlation is 4 bytes, iterate on the rest of the message
            pearson_correlation = np.zeros(len(message[4:]) // 4)
            for i in range(len(pearson_correlation)):
                pearson_correlation[i] = self.byte_to_float(message[4 + 4*i : 4 + 4*i + 4])
        else:
            window_size = -1
            pearson_correlation = []
        return window_size, pearson_correlation
    
    def get_pearson_correlation_at_time_point(self, window_size, timepoint):
        """
        Send: tGetPearsonCorrelationAtTimePoint
        Receive: int WindowSize, int TimePoint, float PearsonCorrelationAtTimePoint
        Provides the Pearson correlation at the time point.
        """
        rOK, aOK, message = self.tbv_client.query('tGetPearsonCorrelationAtTimePoint', [window_size, timepoint])
        
        if rOK and aOK:
            window_size = int.from_bytes(message[:4], byteorder="big")
            timepoint = int.from_bytes(message[4:8], byteorder="big")

            pearson_correlation_at_time_point = np.zeros(len(message[8:]) // 4)
            for i in range(len(pearson_correlation_at_time_point)):
                pearson_correlation_at_time_point[i] = self.byte_to_float(message[8 + 4*i:8 + 4*i + 4])
        else:
            window_size = -1
            timepoint = -1
            pearson_correlation_at_time_point = -1
        return pearson_correlation_at_time_point

    def get_partial_correlation(self, window_size):
        """
        Send: tGetPartialCorrelation
        Receive: int WindowSize, float PartialCorrelation
        Provides the partial correlation.
        """
        rOK, aOK, message = self.tbv_client.query('tGetPartialCorrelation', [window_size])
        if rOK and aOK:
            window_size = int.from_bytes(message[:4], byteorder="big")
            # each correlation is 4 bytes, iterate on the rest of the message
            partial_correlation = np.zeros(len(message[4:]) // 4)
            for i in range(len(partial_correlation)):
                partial_correlation[i] = self.byte_to_float(message[4 + 4*i:4 + 4*i + 4])
        else:
            window_size = -1
            partial_correlation = []
        return window_size, partial_correlation
    
    def get_partial_correlation_at_time_point(self, window_size, timepoint):
        """
        Send: tGetPartialCorrelationAtTimePoint
        Receive: int WindowSize, int TimePoint, float PartialCorrelationAtTimePoint
        Provides the partial correlation at the time point.
        """
        rOK, aOK, message = self.tbv_client.query('tGetPartialCorrelationAtTimePoint', [window_size, timepoint])
        if rOK and aOK:
            window_size = int.from_bytes(message[:4], byteorder="big")
            timepoint = int.from_bytes(message[4:8], byteorder="big")
            partial_correlation_at_time_point = np.zeros(len(message[8:]) // 4)
            for i in range(len(partial_correlation_at_time_point)):
                partial_correlation_at_time_point[i] = self.byte_to_float(message[8 + 4*i:8 + 4*i + 4])
        else:
            window_size = -1
            timepoint = -1
            partial_correlation_at_time_point = -1
        return window_size, timepoint, partial_correlation_at_time_point



# Example usage
if __name__ == "__main__":
    tbv_client = TBVClient('192.168.6.72', 55555)  # Initialize with appropriate parameters
    interface = TBVNetworkInterface(tbv_client)
    interface.create_connection()

    project_name = interface.get_project_name()
    tt = interface.get_current_time_point()
    expected_nr_of_time_points = interface.get_expected_nr_of_time_points()

    print(f'Project name: {project_name}')
    print(f'Current time point: {tt}')
    print(f'Expected number of time points: {expected_nr_of_time_points}')
    print('--------------------------------------')
    tt = 0
    while tt < expected_nr_of_time_points:
        print(f'Current time point: {tt}')
        tt = interface.get_current_time_point()

        # print the number of ROIs
        nr_of_rois = interface.get_nr_of_rois()
        print(f'Number of ROIs: {nr_of_rois}')

        # print the mean of the first ROI at the current time point
        roi, timepoint, mean_of_roi_at_time_point = interface.get_mean_of_roi_at_time_point(0, tt-1)
        print(f'Mean of ROI {roi} at time point {timepoint}: {mean_of_roi_at_time_point}')

        # print the mean of the second ROI at the current time point
        roi, timepoint, mean_of_roi_at_time_point = interface.get_mean_of_roi_at_time_point(1, tt-1)
        print(f'Mean of ROI {roi} at time point {timepoint}: {mean_of_roi_at_time_point}')

        # get the pearson correlation at the current time point with window size 5
        window_size, timepoint, pearson_correlation_at_time_point = interface.get_pearson_correlation_at_time_point(5, tt-1)
        #print(f'Pearson correlation at time point {tt} with window size {window_size}: {pearson_correlation_at_time_point}')

        time.sleep(2)

    interface.close_connection()
