% Q2.m
% Student Name: Sharvan Saikumar
% Student ID: 33918236
% Date: 05/10/2024 (last updated)

fprintf("\n\n--- Q2 --- \n")
%% DO NOT use clear all; close all; clc; and do not rename this file
% Some code may already be provided below
% Apply good programming practices

%% Part A

% finding self-sufficiency data, and other analysis.
selfSuff = ownConsumption_kWh ./ totalConsumption_kWh;
numSelfSuff = sum(selfSuff > 0.5);
averageProd = mean(production_kWh(selfSuff > 0.5));

figure(2); % second figure.

hold on;
grid on;

% plot self suff against dates.
plot(dates, selfSuff*100, 'b-');

% plot horizontal threshold line.
yline(50, 'r--', "50% Self-Sufficiency");
hold off;

% labels, axis, ...
xlabel("Time (Month-Year)");
ylabel("Self-Sufficiency Ratio (%)");
title("Self-Sufficiency Trend");
legend("Self-Sufficiency")
xtickformat('MMM-yyyy');
xticks(dates(1):calmonths(6):dates(end));

% printing statements.
fprintf("\n\nPART A\n");
fprintf("Number of days with self-sufficiency ratio over 50%%: %d\n", numSelfSuff);
fprintf("Average energy production for those days is %.4f kWh\n\n", averageProd);

%% Part B

% calculating savings and earnings.
gridCost_dkWh = gridCost_ckWh / 100;
tariff_dkWh = tariff_ckWh / 100;
savings_d = ownConsumption_kWh .* gridCost_dkWh;
earnings_d = zeros(size(energyOut));

% iterating until the end of dataset.
for i = 1:length(energyOut)
    if dates(i) <= datetime('30-Jul-23', 'InputFormat', 'dd-MMM-yy') % flat rate up to july 31 2023.
        earnings_d(i) = energyOut(i) * tariff_dkWh(i);
    else
    
        if energyOut(i) <= 10 % flat rate applies
            earnings_d(i) = energyOut(i) * tariff_dkWh(i);
        
        else % proportionality applies
            earnings_d(i) = ((energyOut(i) - 10) / 100) + 0.88;

        end
    end
end

% calculating total savings and earnings.
totalSavings = sum(savings_d);
totalEarnings = sum(earnings_d);

% printing statements.
fprintf("\n\nPART B\n");
fprintf("Total Savings made: $%.4f\n", totalSavings);
fprintf("Total Earnings made: $%.4f\n\n", totalEarnings);

%% Part C

% calculating the cumulative return over time.
returns = savings_d + earnings_d;
cumReturns = cumsum(returns);

% fitting linear reg.
daysInd = (1:length(cumReturns)) - 1;
linregCoeff = polyfit(daysInd, cumReturns, 1); % linear line.
values = (polyval(linregCoeff, daysInd))'; % transposed to match dimensions.

% finding payoff day.
f = @(x) linregCoeff(1)*x + linregCoeff(2) -15000; % anonymous function to find payoff day.
payoff = fzero(f,0); % fzero() finds the root of the func defined.
estimatedDayPayoff = round(payoff); % rounding it as it we only want day.
payoffDate = dates(1) + days(estimatedDayPayoff-1); % adjusting for zero index. 

figure(3); % third figure.

hold on;
grid on;

% plot cumulative returns against days.
plot(daysInd, cumReturns, 'b-');

% plot linear reg.
plot(daysInd, values, 'r-');
hold off;

% legends, labels, ...
xlabel("Days Since Start");
ylabel("Cumulative Returns ($)");
legend("Cumulative Returns", "Linear Regression");
title("Cumulative Returns Trend");

% printing results.
fprintf("\n\nPART C\n");
fprintf("The estimated pay-off date modelled with linear regression: %s\n", string(payoffDate));

%% Part D
fprintf("\n\nPART D\n");
fprintf("\nThe Linear Regression model assumes a constant rate of return, but solar power generation and grid costs can fluctuate during different seasons which can lead to price changes.\n");
fprintf("The issue with prediction assumes that returns remain steady over time, and unexpected events like system maintenance or changes in energy prices can impact the pay-off period.\n");

% --------------------- END OF FILE -------------------------