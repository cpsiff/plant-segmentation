%% Runs MultiLeafTracking on given testing images

csv_file = "CVPPP2017_LSC_training/training/A1/A1.csv";

file_names = readtable(csv_file);
file_names = table2array(file_names(:,1));
num_img = size(file_names);

% without creating txt files for data_readInputTextFile.m, or preprocessing
% images with a tight cropping, all images treated the same, where:
% `plant_row, plant_column, location_row, location_column, height, width`
%
% corresponded to:
% 1 1 1 1 size(img, 1) size(img, 2)

for i = 1:num_img
    Filenames = "CVPPP2017_LSC_training/training/A1/" + file_names(i, :);
    img = imread(Filenames);
    dimension_img = size(img);

    img = im2gray(img);
    
    nPlant = 1;
    plantIDs = [1, 1];
    height = dimension_img(1);
    width = dimension_img(2);
    
    % pre-crop image assuming centered
    crop_ratio = .50;
    start_height = round(height * (1 - crop_ratio) / 2);
    end_height = round(height - start_height);
    start_width = round(width * (1 - crop_ratio) / 2);
    end_width = round (width - start_width);
    full_height = end_height - start_height;
    full_width = end_width - start_width;
    PlantLocations = [start_height, start_width, full_height, full_width];
   % PlantLocations = [181, 109, 210, 230];

    %% Changes to MultiLeafTracking:
    % altered input arguments of MultiLeafTracking to circumvent creation 
    % of text file for all images, saving combined mask as fg image.
    %
    % threshold changed from 0.002 to 0.3
  
    
    [mask] = MultiLeafTracking(nPlant, plantIDs, PlantLocations, img);
    % figure, imshow(combinedMask), title('comboMask');
    
    
    file_name_to_fg = replace(file_names(i, :), "rgb", "fg");
    imwrite(logical(mask), "CVPPP2017_LSC_training/fluorescent_method/A1/" + file_name_to_fg);
end
