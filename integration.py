# -*- coding: utf-8 -*-
import numpy as np

class ExpSinhQuadrature():
    def __init__(self, init_step_size, error_tol, max_iter):
        self.init_step_size = init_step_size
        self.error_tol = error_tol
        self.max_iter = max_iter
        
        self.step_size = self.init_step_size
            
    def __call__(self, func):
        new_estimate = 0
        old_estimate = 0
        self.step_size = self.init_step_size

        for n in range(self.max_iter):
            old_estimate = new_estimate;
            new_estimate = self.compute_integral(func)
    
            if abs(old_estimate - new_estimate) < self.error_tol:
                break
            else:
                self.step_size /= 2
        
        return new_estimate

    def abscissa(self, n):
        return np.exp(np.pi / 2. * np.sinh(n * self.step_size))

    def weight(self, n):
        return np.pi / 2. * np.cosh(n * self.step_size) * self.abscissa(n)

    def eval_transformed_func(self, func, n):
        return self.weight(n) * func(self.abscissa(n))

    def compute_integral(self, func):
        # Positive n
        new_term = 0
        threshold = 0
        positive_n_sum = 0
    
        for n in range(1, self.max_iter):
            old_term = new_term;
            new_term = self.eval_transformed_func(func, n);
            
            if abs(new_term - old_term) < threshold and n >= 2:
                break
            else: 
                positive_n_sum += new_term;
                threshold = abs(positive_n_sum * self.error_tol)
    
        # Negative n
        new_term = threshold = 0;
        negative_n_sum = 0;
        for n in range(-1, -self.max_iter, -1):
            old_term = new_term
            new_term = self.eval_transformed_func(func, n)
    
            if abs(new_term - old_term) < threshold and n <= -2:
                break
            else:
                negative_n_sum += new_term;
                threshold = abs(negative_n_sum * self.error_tol)
        
        # Zero n
        zero_n_sum = self.eval_transformed_func(func, 0);
    
        return self.step_size * (negative_n_sum + zero_n_sum + positive_n_sum)

#def f(x): return np.exp(-x)
#rule = ExpSinhQuadrature(0.5, 1e-4, 1000)
#rule(f)