%--------------------------- Script description---------------------------%
% Purpose: Notifying the user that the run had ended
% Created: 1/23/18 by Or Perlman (or@ieee.org)
% Notes: Display a "T" image and makes a "gong" sound using matlab's innert
%        sound files
%-------------------------------------------------------------------------%

%Displaying a "T" image
imagesc([1 1 1;0 1 0;0 1 0])
title('Time is up!!!','FontSize',15)
axis off

%Sounding a gong or a "haleluja - handel" sound
% load handel.mat; %loaded as y
Temp= load('gong.mat');%loaded as y
sound(Temp.y, 2*Temp.Fs);
clear Temp
  
