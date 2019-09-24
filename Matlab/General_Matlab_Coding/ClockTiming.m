
%Storing current time
t1=clock;
      
%---------------------------------%
% The script body goes here.....
%- - - - - - - - - - - - - - - - - 
%---------------------------------%


%Calculating runtime
t2=clock;
RunTime=etime(t2,t1);

%Displaying the runtime:
if RunTime<60 %if less than a minute 
	disp(['RunTime = ',num2str(RunTime),'sec'])
elseif RunTime<3600 % if less than an hour
	disp(['RunTime = ',num2str(RunTime/60), 'min'])
else % If took more than an hour
	disp(['RunTime = ',num2str(RunTime/3600),' hour'])	
end
