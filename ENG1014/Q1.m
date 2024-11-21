% Q1.m
% Student Name: Sharvan Saikumar
% Student ID: 33918236
% Date: 05/10/2024 (last updated)

fprintf("--- Q1 --- \n")
%% DO NOT use clear all; close all; clc; and do not rename this file
% Some code may already be provided below
% Apply good programming practices

%% Part A

% importing dataset into our program.
solarDataSet = importdata("Solar panel raw data_Rev1.csv");

%% Part B

% retrieving the production, total consumption and own consumption.
production_kWh = solarDataSet.data(:, 1) / 1000;
totalConsumption_kWh = solarDataSet.data(:, 2) / 1000;
ownConsumption_kWh = solarDataSet.data(:, 3) / 1000;

% converting string dates into datetime objects to use built-in functions
% for date calculations.
dates = solarDataSet.textdata(2:end, 1);
dates = datetime(dates, 'InputFormat', 'dd-MMM-yy');

% retrieving cost from grid, tariff.
gridCost_ckWh = solarDataSet.data(:, 4);
tariff_ckWh = solarDataSet.data(:, 5);

% plotting figure.
figure(1);

% subplot 1 config.
subplot(2,1,1); % first subplot.
grid on;
hold on; 

% plot production against dates.
plot(dates, production_kWh, 'r');

% plot total consumption against dates.
plot(dates, totalConsumption_kWh, 'b');

% plot own consumption against dates.
plot(dates, ownConsumption_kWh, 'g');
hold off;

% add labels, legends, titles, ...
xlabel("Time (Month-Year)");
ylabel("Energy (kWh)");
title("Energy Production and Consumption Trends");
legend("Production", "Total Consumption", "Own Consumption");
xtickformat('MMM-yyyy');
xticks(dates(1):calmonths(6):dates(end)); % calcmonths(n) allows to increment dates by whole n months of varying lengths of days.


% subplot 2 config.
subplot(2,1,2); % second subplot.
grid on;
hold on;

% plot grid cost against dates.
plot(dates, gridCost_ckWh, 'm');

% plot tariff against dates.
plot(dates, tariff_ckWh, 'k');
hold off;

% add labels, legends, titles, ...
xlabel("Time (Month-Year)");
ylabel("Cost (c-kWh)");
title("Cost from Grid and Tariff Trends");
legend("Cost From Grid", "Feed In Tariff");
xtickformat('MMM-yyyy');
xticks(dates(1):calmonths(6):dates(end)); % same purpose again here.

%% Part C

% using sum aggregation + logicals for quick calculations.
powerOutages = sum( (production_kWh == 0) & (totalConsumption_kWh == 0) & (ownConsumption_kWh == 0) );
solarOffline = sum( (production_kWh == 0) & (totalConsumption_kWh > 0) );

% print statements.
fprintf("\n\nPART C\n");
fprintf("Number of days affected by power outages: %d\n", powerOutages);
fprintf("Number of days affected by offline solar panels: %d\n\n", solarOffline);

%% Part D

% calculating energy in and energy out.
energyIn = totalConsumption_kWh - ownConsumption_kWh;
energyOut = production_kWh - ownConsumption_kWh;

% getting the maximums of each vector.
[maxIn, indexIn] = max(energyIn);
[maxOut, indexOut] = max(energyOut);

% print statements.
fprintf("\n\nPART D\n");
fprintf("Maximum energy of %.4f kWh inflowed at %s\n", maxIn, string(dates(indexIn))); % using string() to covnert datetime to string.
fprintf("Maximum energy of %.4f kWh outflowed at %s\n\n", maxOut, string(dates(indexOut))); % same reason here.

% ---------- END OF FILE --------------