function [Mask]=DelineateMask(Im)
% function [Mask]=DelineateMask(Im)
% Purpose: creaing a logical image Mask
% Created on 08/09/18 by Or Perlman (or@ieee.org)
% Notes
% Change log: 10/02/18 - function name changed (OP)
% Change log: 03/11/18 - added fixed circle/square option (OP)
% Change log: 03/13/18 - allowed user defined mask radius (OP)

%------------------------input variables-------------------------------------%
% Im - 2D image matrix of double
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% Mask.mat - a.mat file containing the 2D logical matrix
%----------------------------------------------------------------------------%

%Satisfaction (from mask) flag
SatisFlag=0;

%Normalizing Im to [0,1]
Im=Im-min(Im(:));
Im=Im./max(Im(:));

%Intial threshold set to 0
Thresh=0;

%Intial Mask set to 1
Mask=ones(size(Im));

%Keep masking until the user is satisfied
while ~SatisFlag
    
    %Displaying input image
    figure
    imagesc(Im,[Thresh 1]);
    title('Current Im')
    colorbar
    colormap(gray)
    
    
    disp('How would you like to create the mask?')
    disp('(1) Manually - free hand')
    disp('(2) Manually - flexible polygon');
    disp('(3) Using a threshold');
    disp('(4) Using a fixed circle');
    disp('(5) Using a fixed square');
    
    MaskCreateMethod=input('--> ');
    
    
    switch MaskCreateMethod
        %Manual Masking - free hand
        case 1
            h=imfreehand;
            Mask=Mask.*createMask(h); % Multiply to get a unity of all masks generated so far
            
        case 2 % Manual Masking - polygon
            h=impoly;
            Mask=Mask.*createMask(h);%Multiply to get a unity of all masks generated so far
            
        case 3
            imcontrast
            Thresh=input('Please indicate a threshold for Mask -- > ');
            Mask=Mask.*Im>Thresh; % 1 where image > threshold, Multiply to get a unity of all masks generated so far
            
        case 4
            title('Specify radius (0) or measure it (1)? (0/1) -->')
            Measure_or_specify=input('Specify radius (0) or measure it (1)? (0/1) -->');
            if Measure_or_specify==1
                title('You have 15s to measure radius')
                h_radius=imdistline;
                pause(15)
                radius=getDistance(h_radius);
            else
                title('Please specify radius [pixels] --> ')
                radius=input('Please specify radius [pixels] --> ');
                title('Thank you')
            end
            title(['Thank you. Distance is: ',num2str(radius),'; Please press on circle center'])
            [CenterX,CenterY]=ginput(1);
            title('Thank you. Center stored')
            Mask=PoligonMasking(Im,radius,CenterX,CenterY,'Circle',1,'r');
            
        case 5
            title('Specify radius (0) or measure it (1)? (0/1) -->')
            Measure_or_specify=input('Specify radius (0) or measure it (1)? (0/1) -->');
            if Measure_or_specify==1
                title('You have 15s to measure radius')
                h_radius=imdistline;
                pause(15)
                radius=getDistance(h_radius);
            else
                title('Please specify radius [pixels] --> ')
                radius=input('Please specify radius [pixels] --> ');
                title('Thank you')
            end
            title(['Thank you. Distance is: ',num2str(radius),'; Please press on circle center'])
            [CenterX,CenterY]=ginput(1);
            title('Thank you. Center stored')
            Mask=PoligonMasking(Im,radius,CenterX,CenterY,'Square',1,'r');
            
    end
        
    %Displaying resulting Mask
    subplot(131)
    imagesc(Mask,[0 1]);
    title('Resulting Mask')
    colorbar
    
    %Updating current Im by masking with current mask
    MaskedIm=Im.*double(Mask);
    subplot(132)
    imagesc(MaskedIm,[Thresh 1]);
    axis off
    colorbar
    title('Masked image')
    
    Im(Mask)=0.5;
    subplot(133)
    imagesc(Im,[Thresh 1]);
    axis off
    colorbar
    title('Puting 0.5 in the mask location')
    
    
    SatisFlag=strcmp(input('Are you satisfied from the mask (y/n)?','s'),'y');
end % End of while loop

%---------------------- saving the output mask to current folder------------%
Mask=logical(Mask);
end
