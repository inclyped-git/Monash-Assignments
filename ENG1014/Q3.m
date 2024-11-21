% Q3.m
% Student Name: Sharvan Saikumar
% Student ID: 33918236
% Date: 08/10/2024 (last updated)

fprintf("\n\n--- Q3 --- \n")
%% DO NOT use clear all; close all; clc; and do not rename this file
% Some code may already be provided below
% Apply good programming practices

%% Part A

% extracting all the months,years in the dataset.
months = month(dates);
years = year(dates);

% create unique year-month combination.
uniqueCombos = years * 100 + months;

% get unique year-month combinations to define months in dataset.
[uniqueMonths, ~, index] = unique(uniqueCombos); % removes duplicates of month-year combos and keeps unique ones only, also returns the indexes of where the unique values occured.

% pre-allocate to save mem.
monthlyProduction = zeros(size(uniqueMonths));
monthlyTotalConsumption = zeros(size(uniqueMonths));
monthlyOwnConsumption = zeros(size(uniqueMonths));

% loop over each unique month and sum the values for that month.
for i = 1:length(uniqueMonths)
    monthlyProduction(i) = sum(production_kWh(index == i));
    monthlyTotalConsumption(i) = sum(totalConsumption_kWh(index == i));
    monthlyOwnConsumption(i) = sum(ownConsumption_kWh(index == i));
end

% calculating back unique month-year combos for plot.
uniqueYears = floor(uniqueMonths / 100);
uniqueMonthNumbers = mod(uniqueMonths, 100);

uniqueDateTimes = datetime(uniqueYears, uniqueMonthNumbers, 1); % converting back to datetime object.

%% Part B

% finding monthly energy out and energy in.
monthlyEnergyOut = monthlyProduction - monthlyOwnConsumption;
monthlyEnergyIn = monthlyTotalConsumption - monthlyOwnConsumption;

figure(4); % figure 4 config.

subplot(2,1,1); % subplot 1.
bar(uniqueDateTimes, monthlyEnergyOut, 'r'); % plotting energy out monthly.
ylabel("Energy Out (kWh)");
xlabel("Date (MMM YY)");
title("Monthly Energy Out");
grid on;
xticks(uniqueDateTimes(3):calmonths(6):uniqueDateTimes(end));
xtickformat('MMM yy');

subplot(2,1,2); % subplot 2.
bar(uniqueDateTimes, monthlyEnergyIn, 'b'); % plotting energy in monthly.
ylabel("Energy In (kWh)");
title("Monthly Energy In");
xlabel("Date (MMM YY)");
grid on;
xticks(uniqueDateTimes(3):calmonths(6):uniqueDateTimes(end));
xtickformat('MMM yy');

%% Part C
fprintf("\n\nPART C\n");
fprintf("\nThe general trend shown here is that the monthly energy outputs is high during summer times and the amount of electricity used from the grid is reduced heavily.\n");
fprintf("During the winter seasons, the monthly energy in is higher as sunlight is less and therefore there is production of electricity from solar panels, and more energy is needed from the grid.\n");

% --------------------- END OF FILE ---------------------