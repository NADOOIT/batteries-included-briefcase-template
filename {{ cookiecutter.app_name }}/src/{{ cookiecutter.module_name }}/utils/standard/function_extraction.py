import os
import ast
from typing import List, Tuple, Set


def separate_functions(file_path: str) -> None:
    print(f"Processing file: {file_path}")

    with open(file_path, "r") as file:
        code = file.read()

    functions = extract_functions(code)
    num_functions = len(functions)
    print(f"Found {num_functions} functions in the file.")

    directory = os.path.dirname(file_path)
    for i, func in enumerate(functions, start=1):
        func_name, func_code, func_imports = func
        func_file_path = os.path.join(directory, f"{func_name}.py")

        if os.path.exists(func_file_path):
            print(f"Skipping function '{func_name}' as the file already exists.")
            continue

        print(f"Processing function '{func_name}' ({i}/{num_functions})...")
        create_function_file(func_file_path, func_name, func_code, func_imports)

    print("Creating/updating __init__.py file with imports...")
    create_init_file(directory, functions)

    print("Done!")


def extract_functions(code: str) -> List[Tuple[str, str, Set[str]]]:
    tree = ast.parse(code)
    functions = []
    imports = extract_imports(code, tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_code = ast.get_source_segment(code, node)
            func_imports = find_function_imports(node, imports)
            functions.append((func_name, func_code, func_imports))

    return functions


def extract_imports(code: str, tree: ast.AST) -> Set[str]:
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_code = ast.get_source_segment(code, node)
            imports.add(import_code)
    return imports


def find_function_imports(func_node: ast.FunctionDef, imports: Set[str]) -> Set[str]:
    func_imports = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name):
            for imp in imports:
                if node.id in imp:
                    func_imports.add(imp)
    return func_imports


def create_function_file(
    file_path: str, func_name: str, func_code: str, func_imports: Set[str]
) -> None:
    with open(file_path, "w") as file:
        file.write("\n".join(func_imports) + "\n\n" + func_code)


def create_init_file(
    directory: str, functions: List[Tuple[str, str, Set[str]]]
) -> None:
    init_file_path = os.path.join(directory, "__init__.py")
    imports = [f"from .{func_name} import {func_name}" for func_name, _, _ in functions]

    if os.path.exists(init_file_path):
        with open(init_file_path, "r") as file:
            existing_imports = file.readlines()

        # Remove existing imports
        imports = [imp for imp in imports if imp not in existing_imports]

        # Combine existing and new imports
        imports = existing_imports + imports

    with open(init_file_path, "w") as file:
        file.write("\n".join(imports))


if __name__ == "__main__":
    file_path = input("Enter the path to the file containing functions: ")
    separate_functions(file_path)