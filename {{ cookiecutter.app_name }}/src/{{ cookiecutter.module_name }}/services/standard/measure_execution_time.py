from datetime import datetime

def measure_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        #print(f"Die Funktion '{func.__name__}' hat {execution_time:.2f} Sekunden gedauert.")
        return result
    return wrapper