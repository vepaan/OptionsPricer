from math import *
from scipy.stats import norm
import matplotlib.pyplot as plt
import tkinter as tk
from numpy import *
import monte_carlo

def n(x):
    if x>=0: return norm.cdf(x)
    else: return 1-norm.cdf(-x)

def pricer(s,x,v,r,q,t):
    v=v/100
    r=r/100
    q=q/100
    d1=(log(s/x)+(r-q+(v**2)/2)*t)/(v*sqrt(t))
    d2=d1-v*sqrt(t)
    c=s*n(d1)*(e**(-q*t))-x*(e**(-r*t))*n(d2)
    p=x*(e**(-r*t))*n(-d2)-s*n(-d1)*(e**(-q*t))
    return c,p

def monte_carlo_pricer(s, x, v, r, q, t, num_simulations):
    call_price, put_price = monte_carlo.monte_carlo_pricer(s, x, v, r, q, t, num_simulations)
    return call_price, put_price

root = tk.Tk()
root.title("Options Pricing Calculator")

tk.Label(root, text="Current Stock Price (S):").grid(row=0, column=0, padx=10, pady=10)
s_entry = tk.Entry(root)
s_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Strike Price (X):").grid(row=1, column=0, padx=10, pady=10)
x_entry = tk.Entry(root)
x_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Volatility (V):").grid(row=2, column=0, padx=10, pady=10)
v_entry = tk.Entry(root)
v_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Risk-free Rate (R):").grid(row=3, column=0, padx=10, pady=10)
r_entry = tk.Entry(root)
r_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Dividend Yield (Q):").grid(row=4, column=0, padx=10, pady=10)
q_entry = tk.Entry(root)
q_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="Time to Maturity (T):").grid(row=5, column=0, padx=10, pady=10)
t_entry = tk.Entry(root)
t_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="Number of simulations (Monte-Carlo model):").grid(row=6, column=0, padx=10, pady=10)
num_entry = tk.Entry(root)
num_entry.grid(row=6, column=1, padx=10, pady=10)

def calculate():
    s = float(s_entry.get())
    x = float(x_entry.get())
    v = float(v_entry.get())
    r = float(r_entry.get())
    q = float(q_entry.get())
    t = float(t_entry.get())
    num_simulations = int(num_entry.get())
    
    c1, p1 = pricer(s, x, v, r, q, t)
    c2, p2 = monte_carlo_pricer(s, x, v, r, q, t, num_simulations)
    
    black_scholes_call_price_label.config(text=f"Black-Scholes Call Price: ${c1:.2f}")
    black_scholes_put_price_label.config(text=f"Black-Scholes Put Price: ${p1:.2f}")
    monte_carlo_call_price_label.config(text=f"Monte-Carlo Call Price: ${c2:.2f}")
    monte_carlo_put_price_label.config(text=f"Monte-Carlo Put Price: ${p2:.2f}")

def monte_carlo_simulation():
    s = float(s_entry.get())
    x = float(x_entry.get())
    v = float(v_entry.get())
    r = float(r_entry.get())
    q = float(q_entry.get())
    t = float(t_entry.get())
    num_simulations = int(num_entry.get())
    
    # Call the C++ Monte Carlo simulation function
    monte_carlo.monte_carlo_simulator(s, v, r, q, t, num_simulations)


#this will let us see how volatility of the underlying stock impacts the option price
def plot_volatility_vs_price(s, x, r, q, t):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x_vals = []
    y_vals_call = []
    y_vals_put = []
    
    for volatility in range(2, 101, 2):
        c, p = pricer(s, x, volatility, r, q, t)
        x_vals.append(volatility)
        y_vals_call.append(c)
        y_vals_put.append(p)
    
    ax.plot(x_vals, y_vals_call, label='Call Price', color='b')
    ax.plot(x_vals, y_vals_put, label='Put Price', color='r')
    
    ax.set_title('Call and Put Prices vs Volatility')
    ax.set_xlabel('Volatility (%)')
    ax.set_ylabel('Price')
    ax.grid(True)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

#this will let us see how risk-free-rate in the market impacts the option price
def plot_rate_vs_price(s, x, v, q, t):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x_vals = []
    y_vals_call = []
    y_vals_put = []
    
    for rate in range(2, 101, 2):
        c, p = pricer(s, x, v, rate, q, t)
        x_vals.append(rate)
        y_vals_call.append(c)
        y_vals_put.append(p)
    
    ax.plot(x_vals, y_vals_call, label='Call Price', color='b')
    ax.plot(x_vals, y_vals_put, label='Put Price', color='r')
    
    ax.set_title('Call and Put Prices vs Risk-free-Rate')
    ax.set_xlabel('Risk-free-Rate (%)')
    ax.set_ylabel('Price')
    ax.grid(True)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

#this will let us see how the dividend paid by the underlying stock impacts the option price
def plot_dividend_vs_price(s, x, r, v, t):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x_vals = []
    y_vals_call = []
    y_vals_put = []
    
    for dividend in range(2, 101, 2):
        c, p = pricer(s, x, v, r, dividend, t)
        x_vals.append(dividend)
        y_vals_call.append(c)
        y_vals_put.append(p)
    
    ax.plot(x_vals, y_vals_call, label='Call Price', color='b')
    ax.plot(x_vals, y_vals_put, label='Put Price', color='r')
    
    ax.set_title('Call and Put Prices vs Dividend Rate')
    ax.set_xlabel('Dividend Rate(%)')
    ax.set_ylabel('Price')
    ax.grid(True)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

def on_vary_volatility():
    plot_volatility_vs_price(
        s=float(s_entry.get()),
        x=float(x_entry.get()),
        r=float(r_entry.get()),
        q=float(q_entry.get()),
        t=float(t_entry.get())
    )

def on_vary_rate():
    plot_rate_vs_price(
        s=float(s_entry.get()),
        x=float(x_entry.get()),
        v=float(r_entry.get()),
        q=float(q_entry.get()),
        t=float(t_entry.get())
    )

def on_vary_dividend():
    plot_dividend_vs_price(
        s=float(s_entry.get()),
        x=float(x_entry.get()),
        v=float(r_entry.get()),
        r=float(q_entry.get()),
        t=float(t_entry.get())
    )


calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

vary_volatility_button = tk.Button(root, text="Vary Volatility", command=on_vary_volatility)
vary_volatility_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

vary_rate_button = tk.Button(root, text="Vary Risk-free-Rate", command=on_vary_rate)
vary_rate_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

vary_div_button = tk.Button(root, text="Vary Dividend Rate", command=on_vary_dividend)
vary_div_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

monte_carlo_button = tk.Button(root, text="View Monte-Carlo simulation", command=monte_carlo_simulation)
monte_carlo_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)


black_scholes_call_price_label = tk.Label(root, text="Black-Scholes Call Price: $0.00")
black_scholes_call_price_label.grid(row=12, column=0, padx=10, pady=10)

black_scholes_put_price_label = tk.Label(root, text="Black-Scholes Put Price: $0.00")
black_scholes_put_price_label.grid(row=12, column=1, padx=10, pady=10)

monte_carlo_call_price_label = tk.Label(root, text="Monte-Carlo Call Price: $0.00")
monte_carlo_call_price_label.grid(row=13, column=0, padx=0, pady=1)

monte_carlo_put_price_label = tk.Label(root, text="Monte-Carlo Put Price: $0.00")
monte_carlo_put_price_label.grid(row=13, column=1, padx=0, pady=1)

root.mainloop()