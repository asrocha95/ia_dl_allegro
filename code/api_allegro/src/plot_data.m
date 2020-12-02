close all; clear; clc;

load my_model/tot_reward_hist.csv

reward = tot_reward_hist';
l = length(reward);



avg_last_100 = zeros(l,1);

for i=1:l
    if i<=100
        avg_last_100(i) = sum(reward(1:i))/i;
    else
        avg_last_100(i) = sum(reward(i-100:i))/100;
    end
end

figure
plot(reward(1:6e3),'r')
title('Recompensa total por episódio')

figure
plot(avg_last_100(1:6e3),'b')
title('Recompensa média dos últimos 100 episódios')