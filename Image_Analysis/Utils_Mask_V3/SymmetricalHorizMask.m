function [SymmetHorMask]=SymmetricalHorizMask(Im,Mask)
% function [SymmetHorMask]=SymmetricalHorizMask(Im,Mask)
% Purpose: Creating an horizontally symetrical mask
% Created: 10/01/18 by Or Perlman (or@ieee.org)
% Notes:
%------------------------input variables-------------------------------------%
% Im - the original image on which the mask was created
% Mask - original mask
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% SymmetHorMask - a horizontally symmetrical logica mask (for the input one)
%----------------------------------------------------------------------------%
% Changes log:

%Getting the boundaries of the mask
BW=bwboundaries(Mask);
BW=BW{1};

%Displaying the original image
figure
imagesc(Im)
hold on

%Ploting the input mask boundaries
plot(BW(:,2), BW(:,1), 'k','LineWidth',2);

%Delineating the center of symmetry
title('Please mark the center of symmetry...')
[col_center,~]=ginput(1);
col_center=round(col_center); %rounding (pixel location)
title('Thank you')

%Initizalizing new mask
SymmetHorMask=0.*Mask;

%Coordinates of mask pixels
[row_orig,col_orig]=find(Mask);

%Creating horizontally mirrored mask
for ind=1:length(row_orig)
    
    %Calculating horizontal distance between current mask pixel and the
    %   reference center
    CurDist=col_orig(ind)-col_center;
    
    %Filling new pixel in the mirrored mask
    SymmetHorMask(row_orig(ind),col_center-CurDist)=1;
end

%Conveting mask to logical
SymmetHorMask=logical(SymmetHorMask);

%Getting the boundaries of the mirrored mask
BW_mirrored=bwboundaries(SymmetHorMask);
BW_mirrored=BW_mirrored{1};

%Ploting the mirrored mask boundaries
plot(BW_mirrored(:,2), BW_mirrored(:,1), 'y','LineWidth',2);

end
