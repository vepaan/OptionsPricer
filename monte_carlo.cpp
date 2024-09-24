#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <random>
#include <cmath>
#include <vector>
#include <numeric>
#include <iostream>
#include <matplotlibcpp.h>

namespace py = pybind11;
namespace plt = matplotlibcpp;


double max(double a, double b) {
    return (a > b) ? a : b;
}

std::vector<double> monte_carlo_pricer(double s, double x, double v, double r, double q, double t, int num_simulations) {
    v = v / 100;
    r = r / 100;
    q = q / 100;
    int steps = 100;
    double dt = t / steps;

    std::vector<double> call_prices;
    std::vector<double> put_prices;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1);

    for (int i = 0; i < num_simulations; ++i) {
        double stock_price = s;
        for (int j = 0; j < steps; ++j) {
            double z = d(gen);
            stock_price *= std::exp((r - q - 0.5 * v * v) * dt + v * std::sqrt(dt) * z);
        }

        double call_payoff = max(stock_price - x, 0.0) * std::exp(-r * t);
        double put_payoff = max(x - stock_price, 0.0) * std::exp(-r * t);
        call_prices.push_back(call_payoff);
        put_prices.push_back(put_payoff);
    }

    double call_price_avg = std::accumulate(call_prices.begin(), call_prices.end(), 0.0) / call_prices.size();
    double put_price_avg = std::accumulate(put_prices.begin(), put_prices.end(), 0.0) / put_prices.size();

    return {call_price_avg, put_price_avg};
}

void monte_carlo_simulator(double s, double v, double r, double q, double t, int num_simulations) {
    v = v / 100;
    r = r / 100;
    q = q / 100;
    int steps = 100;
    double dt = t / steps;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1);  

   
    std::vector<std::vector<double>> paths(num_simulations, std::vector<double>(steps + 1));
    for (int i = 0; i < num_simulations; ++i) {
        paths[i][0] = s;  // Initial stock price
        for (int j = 1; j <= steps; ++j) {
            double z = d(gen);
            paths[i][j] = paths[i][j - 1] * std::exp((r - q - 0.5 * v * v) * dt + v * std::sqrt(dt) * z);
        }
    }

    plt::figure_size(800, 400);
    for (const auto& path : paths) {
        plt::plot(path);
    }
    plt::title("Geometric Brownian Motion Paths");
    plt::xlabel("Time Steps");
    plt::ylabel("Stock Price");
    plt::grid(true);
    plt::show();
}

PYBIND11_MODULE(monte_carlo, m) {
    m.doc() = "Monte Carlo simulation module for option pricing";
    
    m.def("monte_carlo_pricer", &monte_carlo_pricer, "Run Monte Carlo simulations for option pricing",
          py::arg("s"), py::arg("x"), py::arg("v"), py::arg("r"), py::arg("q"), py::arg("t"), py::arg("num_simulations"));
    
    m.def("monte_carlo_simulator", &monte_carlo_simulator, "Simulate paths using geometric Brownian motion",
          py::arg("s"), py::arg("v"), py::arg("r"), py::arg("q"), py::arg("t"), py::arg("num_simulations"));
}
