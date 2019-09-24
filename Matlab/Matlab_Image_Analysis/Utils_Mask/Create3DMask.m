function [Mask3D, NumPixelVOI]=Create3DMask(Im3D)
% function []=Create3DMask(Im)
% Purpose: creaing a logical image Mask
% Created on 08/25/18 by Or Perlman (or@ieee.org)
% Notes
% Change log: 2/25/19 added Number of pixels in VOI output (OP)
%------------------------input variables-------------------------------------%
% Im - 3D image matrix of double (sized x dimsnsion, y dimension, num_slices)
%----------------------------------------------------------------------------%
%-----------------------output variables-------------------------------------%
% Mask3D- 3D logical mask 
% NumPixelVOI - number of pixels in VOI
%----------------------------------------------------------------------------%

%Finging number of slices
NumSlices=size(Im3D,3);

%Initializing output 3D mask
Mask3D=zeros(size(Im3D));

for SliceInd=1:NumSlices
    
    %Satisfaction (from mask) flag
    SatisFlag=0;
    
    %Current examined image
    Im=Im3D(:,:,SliceInd);
    
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
        colormap(jet)
        
        
        disp('How would you like to create the mask?')
        disp('(1) Manually - free hand')
        disp('(2) Manually - polygon');
        disp('(3) Using a threshold');
        disp('(4) All mask pixels in this slice should be zeros')
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
                Mask=Mask.*0;
        end
        
        %Displaying resulting Mask
        subplot(121)
        imagesc(Mask,[0 1]);
        title('Resulting Mask')
        colorbar
        
        %Updating current Im by masking with current mask
        Im=Im.*double(Mask);
        subplot(122)
        imagesc(Im,[Thresh 1]);
        axis off
        colorbar
        title('Masked image')
        
        
        SatisFlag=strcmp(input('Are you satisfied from the mask (y/n)?','s'),'y');
        
    end % End of while loop
    
    Mask3D(:,:,SliceInd)=Mask;
    
end % Closes the slices loop

%Number of pixels in VOI
NumPixelVOI=sum(Mask3D(:));

end
