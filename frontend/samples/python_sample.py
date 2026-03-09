"""
Advanced Fibonacci Calculator with memoization
"""
import time
from functools import lru_cache

class FibonacciCalculator:
    """A class to calculate Fibonacci numbers with various optimizations"""
    
    def __init__(self):
        self.cache = {}
        self.recursive_calls = 0
    
    @lru_cache(maxsize=128)
    def fibonacci_recursive(self, n):
        """Calculate Fibonacci recursively with caching"""
        self.recursive_calls += 1
        
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n
        
        return self.fibonacci_recursive(n-1) + self.fibonacci_recursive(n-2)
    
    def fibonacci_iterative(self, n):
        """Calculate Fibonacci iteratively"""
        if n < 0:
            raise ValueError("n must be non-negative")
        
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def fibonacci_generator(self, limit):
        """Generate Fibonacci sequence up to limit"""
        a, b = 0, 1
        count = 0
        
        while count < limit:
            yield a
            a, b = b, a + b
            count += 1

def main():
    # Create calculator instance
    calc = FibonacciCalculator()
    
    # Test different implementations
    n = 35
    
    # Recursive with caching
    start = time.time()
    result_rec = calc.fibonacci_recursive(n)
    time_rec = time.time() - start
    
    # Iterative
    start = time.time()
    result_iter = calc.fibonacci_iterative(n)
    time_iter = time.time() - start
    
    print(f"Fibonacci({n}) = {result_rec}")
    print(f"Recursive calls: {calc.recursive_calls}")
    print(f"Recursive time: {time_rec:.4f}s")
    print(f"Iterative time: {time_iter:.4f}s")
    
    # Generate sequence
    print("\nFirst 10 Fibonacci numbers:")
    for i, num in enumerate(calc.fibonacci_generator(10)):
        print(f"F{i} = {num}")

if __name__ == "__main__":
    main()