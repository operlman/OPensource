function [Im_Section]= Part_of_Image(Im,CenterImCol,CenterImRow,DistCol,DistRow)
% Purpose: Use a previously delineated coordinates to get a cropped image  
% Created: 07/04/19 by Or Perlman (or@ieee.org)
% Notes:
%------------------------input variables-------------------------------------%
%  Im - original image
% CenterImCol - column coordinate for the center of the cropped image 
% CenterImRow - row coordinate for the center of the cropped image 
% DistCol - length of cropped image columns
% DistRow - length of cropped image DistRow
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
 % Cropped image
%----------------------------------------------------------------------------%
% Changes log:

Im_Section = Im(CenterImRow-DistRow:CenterImRow+DistRow,CenterImCol-DistCol:CenterImCol+DistCol);

end