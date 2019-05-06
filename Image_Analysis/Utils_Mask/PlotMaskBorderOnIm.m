function []=PlotMaskBorderOnIm(Mask,LineColor,LineWidth)
% Purpose: Plot the boundaries of a given mask on a displayed image
% Created: 10/12/18 by OP
% Notes:
%------------------------input variables-------------------------------------%
%  Mask - logical mask (2D)
%  LineColor - string for the line color (e.g. 'y')
%  LineWidth - int for line width (e.g. 2)
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% The line is plotted on the already presented figure
%----------------------------------------------------------------------------%
% Changes log:


%Getting the boundaries of the mirrored mask
BW_mirrored=bwboundaries(Mask);
BW_mirrored=BW_mirrored{1};

%Ploting the mirrored mask boundaries
plot(BW_mirrored(:,2), BW_mirrored(:,1), LineColor,'LineWidth',LineWidth);
 
end