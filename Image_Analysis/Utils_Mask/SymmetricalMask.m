function [SymmetMask]=SymmetricalMask(Im,Mask)
% function [SymmetricalMask]=SymmetricalMask(Im,Mask)
% Purpose: Creating a symetrical mask with respect to a reference point
% Created: 10/12/18 by Or Perlman (or@ieee.org)
% Notes: Requires the function PlotMaskBorderOnIm.m on the same path
%------------------------input variables-------------------------------------%
% Im - the original image on which the mask was created
% Mask - original mask
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% SymmetMask - a symmetrical logica mask (for the input one), with respect
%              to a delineated point
%----------------------------------------------------------------------------%
% Changes log:


%Displaying the original image
figure
imagesc(Im)
hold on

%Ploting the input mask boundaries
PlotMaskBorderOnIm(Mask,'k',2)

%Delineating the center of symmetry
title('Please mark the center of symmetry...')
[col_center,row_center]=ginput(1);
col_center=round(col_center); %rounding (pixel location)
row_center=round(row_center); %rounding (pixel location)
title('Thank you')

%Initizalizing new mask
SymmetMask=0.*Mask;

%Coordinates of mask pixels
[row_orig,col_orig]=find(Mask);

%Creating mirrored symmetrical mask
for ind=1:length(row_orig)
    
    %Calculating x & y distances between current mask pixel and the
    %   reference center
    ColDist=col_orig(ind)-col_center;
    RowDist=row_orig(ind)-row_center;
    
    %Filling new pixel in the mirrored mask
    SymmetMask(row_center-RowDist,col_center-ColDist)=1;
end

%Conveting mask to logical
SymmetMask=logical(SymmetMask);


%Ploting the mirrored mask boundaries
PlotMaskBorderOnIm(SymmetMask,'y',2)


end
