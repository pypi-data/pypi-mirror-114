import numpy as np
from scipy.linalg import expm, solve


def ss_response(size_kw, lower_bound, ramp_rate, a_, b_, c, d):
    """Calculate state space response for a given Component.

    Positional arguments:
    gen - (Component) Component (used to be generator) for which the
        response is to be calculated.
    """
    # Get timestep.
    rr0 = ramp_rate+0
    t_peak = (size_kw - lower_bound) / ramp_rate * 3600
    if t_peak > 4*60:
        dt = 60
    elif t_peak > 3.6e4:
        dt = 3600
    else:
        dt = 1
    # Convert continuous state-space to discrete time state-space.
    a = expm(np.array(a_) * dt).tolist()
    b = (solve(np.array(a_), (a - np.eye(2)))
        @ np.array(b_)).tolist()

    time = 5 * t_peak
    ramp_rate = False
    count = 0
    while isinstance(ramp_rate, bool):
        n_s = int(round(time / dt, 0))
        u = [size_kw] * (n_s + 1)
        x_0 = []
        for i in range(len(c)):
            if c[i] == 1:
                x_0.append(lower_bound)
            else:
                x_0.append(0)
        y, t = ss_sim(a, b, [c], [d], x_0, u, dt)
        norm_end = [abs(y[j][0]-y[-1][0])/y[-1][0] for j in range(len(u)-10,len(u))]
        if (y[-1][0] - y[0][0])/(u[0] - y[0][0]) > 0.95 and max(norm_end)<1e-3:
            n_r = 0
            n_val = 0
            while n_val < 0.95:
                n_r+=1
                n_val = (y[n_r][0] - y[0][0])/(u[0] - y[0][0])
            r = 1-(n_val - .95)/(n_val - (y[n_r-1][0] - y[0][0])/(u[0] - y[0][0]))
            t_rise = (t[n_r-1] + r*(t[n_r] - t[n_r-1]))/3600 #rise time in hours
            ramp_rate = (size_kw - lower_bound)*0.95/t_rise

        else:
            time *= 5
        count += 1
        if count > 10:
            ramp_rate = rr0
    return ramp_rate


def ss_sim(a, b, c, d, x_0, u, dt):
    time = [t*dt for t in range(len(u)+1)]
    x = [[0 for j in range(len(x_0))] for i in range(len(u) + 1)]
    x[0] = x_0
    y = [[0 for j in range(len(c))] for t in range(len(u) + 1)]
    y[0] = [sum([c[j][i] * x_0[i] for i in range(len(x_0))]) for j in range(len(c))]
    for t in range(len(u)):
        x[t+1] = [sum([a[i][j] * x[t][j] for j in range(len(x_0))]) + b[i] * u[t] for i in range(len(a))] 
        y[t+1] = [sum([c[j][i] * x[t+1][i] for i in range(len(c))]) + d[j] * u[t] for j in range(len(c))]
    return y, time
