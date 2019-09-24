%Using a pool of 4 CPUs in parallel if not already connected
if isempty(gcp('nocreate'))
    myCluster=parcluster('local'); myCluster.NumWorkers=4; parpool(myCluster,4)
end

% parfor.... end

% Closing a pool
poolobj = gcp('nocreate');
delete(poolobj); 
