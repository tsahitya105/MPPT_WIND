
a = zeros(1,15000);
b = zeros(1,15000);
lua = 1;

for beta = 25   
    for x = 0.001:0.001:15
        lambdai = (1/(x + 0.08*beta) - 0.035/(1+beta*beta*beta))^(-1);
        y = 0.5*(116*1/lambdai - 0.4*beta - 5)*exp(-21/lambdai);
        a(lua) = x;
        b(lua) = y;
        lua = lua +1;
    end
    plot(a,b);
    hold('on');
    xlabel('tip speed ratio');
    ylabel('coefficient of performance');
    
end
