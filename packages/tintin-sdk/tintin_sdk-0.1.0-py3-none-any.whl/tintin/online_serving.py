import dill
import base64
import os
from typing import Any, Callable


transform_data_file_name = "transform_data.python.byte_code"


# Decorator on function to save it to model
def save_function_to_model(model_path, file_name):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                if os.path.isdir(model_path):
                    file_path = os.path.join(model_path, file_name)
                    function_python_byte_code = dill.dumps(func)
                    with open(file_path, "w") as file_write:
                        file_write.write(base64.b64encode(function_python_byte_code).decode("utf-8"))
                    print("Save function to file path ", file_path)
                else:
                    print("Model path ", model_path, " is not a directory so saving function is skipped.")
            except Exception as e:
                print("Fail to save function from ", model_path, file_name, " with error ", e)
            
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator

# Load function from model
def load_function_from_model(model_path, file_name) -> Callable[..., Any]:
    file_path = os.path.join(model_path, file_name)
    try:
        if os.path.isfile(file_path):
            with open(file_path, "r") as file_read:
                function_python_byte_code = file_read.read()
            func = dill.loads(base64.b64decode(function_python_byte_code.encode("utf-8")))
            return func
        else:
            print("File path ", file_path, " is not a file so fail to load function.")
            return None
    except Exception as e:
        print("Fail to load function from ", model_path, file_name, " with error ", e)
        return None
            
        
