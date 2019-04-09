function [CNR]=CNR(Image,ROIobject,ROIBackground)
% function [CNR]=CNR(ROIobject,ROIBackground)
%This function  was created on  01/05/14 by Or Perlman (or@ieee.org).
%This function's purpose is to calculate contrast to noise ratio (CNR)
%------------------------input variables-------------------------------------%
% Image - the relevant image
% ROIobject - the object ROI (as a logical 1/0  matrix with same size as the image)
% ROIBackground - the Background ROI (as a logical 1/0  matrix with same size as the image)
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
%  CNR - resulting CNR
%----------------------------------------------------------------------------%

%calculating mean intensities
Iobj=mean(Image(ROIobject));
Iback=mean(Image(ROIBackground));
SigObj=var(Image(ROIobject));
Sigback=var(Image(ROIBackground));

CNR=abs(Iobj-Iback)/sqrt(SigObj+Sigback);
end
