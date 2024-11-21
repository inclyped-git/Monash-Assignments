function [root,iter] = falseposition(f, xl, xu, precision)
% [root,iter] = falseposition(f, xl, xu, precision)
% Written by: ???, ID: ???
% Last modified: ???
%
% INPUTS:
%  - f: function handle of the equation to be solved
%  - xl: lower limit of the initial guess/bracket
%  - xu: upper limit of the initial guess/bracket
%  - precision: stopping criteria determined by the user
% OUTPUT:
%  - root: the root of the equation
%  - iter: the number of iterations taken to find the root

% checking if bounds are appropriate
if f(xl)*f(xu) > 0
    error('Bounds are not appropriate')
end

% Estimate 1st iteration of xr and initialise iteration count
iter = 1;
xr = (f(xu)*xl - f(xl)*xu)/(f(xu) - f(xl));

% Check if f(xr) is close enough to zero
while abs(f(xr)) > precision 
    % checking subinterval for root
	if f(xl)*f(xr) < 0
        xu = xr;
    else
        xl = xr;
    end
    % Recalculate xr and update iteration count
    iter = iter + 1;
    xr = (f(xu)*xl - f(xl)*xu)/(f(xu) - f(xl));
end

% The final xr value is the root
root = xr;
