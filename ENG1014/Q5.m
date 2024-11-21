% Q5.m
% Student Name: Sharvan Saikumar
% Student ID: 33918236
% Date: 13/10/2024 (last updated)

fprintf("\n\n--- Q5 --- \n")
%% DO NOT use clear all; close all; clc; and do not rename this file
% Some code may already be provided below
% Apply good programming practices

%% Part A
rotatorRadius = 7 / 2;
rho = 1.204; % source: https://en.wikipedia.org/wiki/Density_of_air
timeSpent = 24 * 60 * 60; % seconds in a day.

coEff = pi * rotatorRadius^2 * timeSpent * rho;
mass_v = @(v) coEff * v;

% printing result.
fprintf("\n\nPART A\n");
fprintf("Anonymous function defined for mass of air swept per day: M(v) = %.4f * v kg\n", coEff);

%{
Calculations for Part A

V/t = A * v
mass = V/t * t * rho
==> mass = A * v * t * rho
m(v) = At*rho*(v)
%}

%% Part B
energyNeeded = 45.0956 * 3.6e6; % 1 kWh = 3.6 MJ
C_p = 0.25;

airVelocity = (2 * energyNeeded) / (C_p * coEff);
airVelocity = airVelocity^(1/3);

fprintf("\n\nPART B\n");
fprintf("Average wind velocity is: %.4f ms^-1\n", airVelocity);

%{
Calculations for Part B

Eout = Cp * Ein
Ein = 0.5 * m(v) * v^2
==> Ein = 0.5 * At*rho*v^3
==> Eout = Cp * 0.5 * At * rho * v^3

==> v^3 = ( 2  * Eout ) / ( Cp * At* rho )
%}

%% Part C

% calculating inertia of the housing.
massHousing = 50;
radiusHousing = 0.5 / 2;
inertiaHousing = massHousing * radiusHousing^2; % assuming thin walled hollow cylinder.

% calculating inertia of the blades.
massBlade = 150;
lengthBlade = rotatorRadius - radiusHousing;

inertiaBladesCOM = (1/12) * massBlade * (lengthBlade)^2; % mL^2 / 12
inertiaBladesParallel = ((lengthBlade) / 2 + radiusHousing)^2 * massBlade; % md^2
inertiaBlades = inertiaBladesCOM + inertiaBladesParallel;

% calculating total inertia.
totalInertia = inertiaHousing + 3*inertiaBlades;

fprintf("\n\nPART C\n");
fprintf("Total inertia of one assembled turbine: %.4f kgm^2\n", totalInertia);

%% Part D

% calculations:
% Erot = 0.3 * Ekinetic
% Eelectric = 0.8333 * Erot
% Eelectric = 0.3 * 0.8333 * Ekinetic

energyElectric = energyNeeded;
energyWindKinetic = energyElectric / (0.3 * 0.8333);
energyRotational = energyWindKinetic * 0.3;

% Erot = 0.5*I*w^2
% w = sqrt(2* Erot / I)
rotVelocity = sqrt(2*energyRotational / (totalInertia));

fprintf("\n\nPART D\n");
fprintf("Average rotational velocity should be: %.4f rads^-1\n", rotVelocity);

%% Part E

% calculations:
% friction = mu * N
% N = m * g
% N = (mhousing + 3*mblades) * g

g = 9.81;
mu = 0.1;

totalMass = massHousing + 3*massBlade;
normalForce = totalMass * g;
friction = normalForce * mu;

fprintf("\n\nPART E\n");
fprintf("The expected friction force is: %.4f N\n", friction);

%% Part F

torque = friction * (0.1);
accel = torque / (totalInertia);

fprintf("\n\nPART F\n");
fprintf("The rotational deceleration acting on the turbines: %.4f rad/s^2\n", accel)

%% Part G
initialVel = 54.67;
time = initialVel / accel;

fprintf("\n\nPART G\n");
fprintf("Time needed to come back to rest: %.4f s\n", initialVel);

% ---------- END OF FILE -----------