close all; clear; clc;

load reward_hist.csv

% plot(reward_hist(:,2),reward_hist(:,3))

reward = reward_hist(:,2:3);
avg_last_100 = zeros(length(reward),1);

for i=1:length(reward)
    if i<=100
        avg_last_100(i) = sum(reward(1:i,2))/i;
    else
        avg_last_100(i) = sum(reward(i-100:i,2))/100;
    end
end

figure
plot(1:length(reward),reward(:,2),'r')

figure
plot(1:length(reward),avg_last_100(:),'b')