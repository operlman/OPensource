%---------------------------------------- script description------------------- ----------------------------------------------%
%This script  was created at  9/7/15 by Or Perlman (or@ieee.org).
%This script was last modified on 2/22/19 by OP
%This script's purpose is to wait a specific time as chosen by the user and
%than activate a specific command
%-----------------------------------------------------------------------------------------------------------------------------%


%creatting a timer object
TheTimer = timer;

%waiting time in sec (converting min to sec by multiplying with 60)
WaitingTime_min=input('Please enter desired waiting time (min):  ');

% WaitingTime_min=60;%(min)
TheTimer.StartDelay=60*WaitingTime_min;

%activating the timer 
%Notify_Time_is_up - a sound and image activated after time ends
TheTimer.TimerFcn = @(TheTimerObj, thisEvent)Notify_Time_is_up; 

start(TheTimer)

%notifying activation to user
disp(['Timer set for ',num2str(WaitingTime_min),' minutes ']);
disp('started at :')
Cur_Time_started=fix(clock)%#ok <disp time>

% arecord test.wav - recording in ubuntu. press ctrl_c to stop. recorded
% wav file will appear in home directory

function [] = Notify_Time_is_up()
%--------------------------- Script description---------------------------%
% Purpose: Notifying the user that the run had ended
% Created: 1/23/18 by Or Perlman (operlman@mgh.harvard.edu)
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
end
