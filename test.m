% Test.m for testing the nnet model.

max_i = input('Enter the max i value, read README.txt for clarification ')

load net

for i = 1:max_i
    x= csvread(strcat('inputs_',int2str(i)));
    t= csvread(strcat('targets_',int2str(i)));
    disp('test inputs and targets read')
    inputs = x';
    targets = t';

    % Test the Network
    outputs = net(inputs);
    % net contains the trained model.

    errors = gsubtract(targets,outputs);
    performance = perform(net,targets,outputs);
    
    trainTargets = targets .* tr.trainMask{1};
    valTargets = targets  .* tr.valMask{1};
    testTargets = targets  .* tr.testMask{1};
    trainPerformance = perform(net,trainTargets,outputs);
    valPerformance = perform(net,valTargets,outputs);
    testPerformance = perform(net,testTargets,outputs);
        
end


