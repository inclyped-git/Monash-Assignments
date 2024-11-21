% Q4.m
% Student Name: REDACTED
% Student ID: REDACTED
% Date: 08/10/2024 (last updated)

fprintf("\n\n--- Q4 --- \n")
%% DO NOT use clear all; close all; clc; and do not rename this file
% Some code may already be provided below
% Apply good programming practices

%% Part A
figure(5) % figure 5 config.

% importing data and retrieving datasets.
dataProductionSet = importdata('Monthly production data.csv');
monthNumber = dataProductionSet.data(:,1);
monthProduction = dataProductionSet.data(:, 2);

% plotting the months and the productions.
plot(monthNumber, monthProduction, 'ro', 'MarkerFaceColor','r');
xlabel("Months");
ylabel("Monthly Production (kWh)");
title("Monthly production data from July 20 - June 22");
hold on;

% curve fitting.
fittedCurve = polyfit(monthNumber, monthProduction, 6);
fittedCurveEval = polyval(fittedCurve, monthNumber);
plot(monthNumber, fittedCurveEval, 'b');
legend("Monthly Production Data", "Fitted Curve");

% model explanation.
fprintf("\n\nPART A\n");
fprintf("I chose a polynomial model using polyfit because it provides a flexible and straightforward approach to fitting non-linear data.\n");
fprintf("This is because the graph was continous as compared to modelling piecewise functions where the data points were not continuous at some points, which makes it difficult for analysis in period of months where the piecewise functions are not defined at.\n\n");

%% Part B
actualProduction = sum(monthProduction); % get the total
fprintf("\n\nPART B\n");
fprintf("\nActual Total Energy Production for Two Years: %.4f kWh\n", actualProduction);

% using numerical integration to get the total production.
% h = (b-a) / (n-1) ==> n = (b-a) / h + 1

% recalculating the points and values to match the segment width.
segmentWidth = 1e-4;
numberOfPoints = (monthNumber(end) - monthNumber(1)) / segmentWidth + 1;
f_x = @(x) polyval(fittedCurve, x);
I_simp13 = comp_simp13(f_x, monthNumber(1), monthNumber(end), numberOfPoints);

% printing calculations.
fprintf("Estimated Total Energy for Two Years: %.4f kWh\n", I_simp13);

% finding error and discussion about the model.
integralError = abs(I_simp13 - actualProduction) * 100 / actualProduction;

% printing calculations.
fprintf("\nThe relative error of the estimated value is: %.4f%%\n", integralError);
fprintf("This tells us that the model we used for the curve fitting is reasonably accurate, but there is a small discrepancy between the actual energy production and the estimate found.\n");
fprintf("The small error implies the polynomial model is generally a good choice for this data, or otherwise we need to implement even higher non-linear polynomial fits to get better precision.\n");

%% Part C

% doing numerical root finding to find ranges above 800 kWh.
func = @(x) polyval(fittedCurve, x) - 800; % root function.
precision = 1e-6;

[root1, ~] = falseposition(func, monthNumber(1), monthNumber(6), precision);
[root2, ~] = falseposition(func, monthNumber(7), monthNumber(12), precision);
[root3, ~] = falseposition(func, monthNumber(13), monthNumber(18), precision);
[root4, ~] = falseposition(func, monthNumber(19), monthNumber(end), precision);

% plotting the ranges.
plot([root1, root2], [800, 800], '-c', 'LineWidth', 3);
plot([root3, root4], [800, 800], '-c', 'LineWidth', 3);
legend("Production Data", "Polyfit Fitted Curve", "Summer Period Range");

startDate = datetime(2020, 7, 1); % start datetime.

summerStart1 = startDate + calmonths(floor(root1) - 7) + days((root1 - floor(root1)) * 30); % summer starts at september so 30 days.
summerEnd1 = startDate + calmonths(floor(root2) - 7) + days( (root2 - floor(root2)) * 28); % summer ends at february so 28 days.

summerStart2 = startDate + calmonths(floor(root3) - 7) + days( ((root3 - floor(root3)) * 31)); % summer starts again at october so 31 days.
summerEnd2 = startDate + calmonths(floor(root4) - 7) + days( ((root4 - floor(root4)) * 28)); % summer ends again at february so 28 days.

% printing answers.
fprintf("\n\nPART C\n");
fprintf("\nThe first summer period starts at %s and ends at %s.\n", string(summerStart1), string(summerEnd1));
fprintf("The second summer period starts at %s and ends at %s.\n", string(summerStart2), string(summerEnd2));

% ---------- END OF TASK -----------
