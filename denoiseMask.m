function [denoised_image] = denoiseMask(binary_mask, w_size, threshold)

% objective: denoise binary mask w moving average filter, then convert
% back into binary mask with some threshold value.

average_filter = fspecial('average', w_size);
denoised_image = imfilter(binary_mask, average_filter, 'replicate');
    
% selects some threshold value to accept as image
    
denoised_image(denoised_image > threshold) = 1;
denoised_image(denoised_image <= threshold) = 0;
    
end