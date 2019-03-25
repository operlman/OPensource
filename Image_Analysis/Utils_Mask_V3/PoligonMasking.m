function [ROImask]=PoligonMasking(image,Radius,CenterX,CenterY,Shape,PlotFlag,ColorPlot)
% function [ROImask]=PoligonMasking(image,Radius,CenterX,CenterY,Shape,PlotFlag)
%This function  was created at  by  Laszlo Balkay (file from MATLAB
%central)
%The function was last modified by Or Perlman (or@ieee.org) at 2/1/14.
%This function's purpose is to perform polygon (circle/square) masking
%------------------------input variables-------------------------------------%
 %Example for input: Radius = 20;CenterX = 50;CenterY = 50;
%  Radius - radius of ROI 
%     (if its a square than the Radius is considered half of the Edge)
% CenterX - x ccordinate of center of poligon
% CenterY - y ccordinate of center of poligon
% image - input image
% Shape - poligon shape ('Circle' or 'Square')
% PlotFlag - 1 if ploting desired, 0 otherwise
% ColorPlot - string of desired color for plot frame
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
%  ROImask - a logical ROI mask (same size as image)
%---------------------------------------------------------------------------------------%
 
% roi Setup
%----------------------------------------------%
if strcmp(Shape,'Circle')
    t = 0:pi/20:2*pi;
    xi = Radius*cos(t)+CenterX;
    yi = Radius*sin(t)+CenterY;
    
else %i.e square shape (in this case radius is full edge
    Edge=2*Radius;
    xi=(CenterX-round(Edge/2)):(CenterX+round(Edge/2));
    xi=[xi repmat(xi(end),1,length(xi)-2) fliplr(xi) repmat(xi(1),1,length(xi)-2)];
    yi=(CenterY-round(Edge/2)):(CenterY+round(Edge/2));
    yi=[repmat(yi(1),1,length(yi)-1) yi repmat(yi(end),1,length(yi)-1) fliplr(yi(1:end-2))];

end
%-------------------------------------------------%

if PlotFlag
LineHandler = line(xi,yi,'LineWidth',3,'Color',ColorPlot);%#ok <using just for ploting>
end

% calc. roi stat.
ROImask = poly2mask(xi,yi, size(image,1),size(image,2));

%display how many pixels are in the ROImask
disp([num2str(sum(ROImask(:)==1)) ' pixels are in the ROI'])

% pr_r = find(roimask);
% roimean = mean(currentimage(pr_r));
% roistd = std(currentimage(pr_r));
% [roimean roistd]
end
