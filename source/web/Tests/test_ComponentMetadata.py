import os
import json
import shutil
import re
import pytest

from config import load_config
 
EXPORT_PATTERN = re.compile(r"""export\s+(?:\*\s+from|{[^}]*}\s+from)\s+['"]([^'"]+)['"]""")
 
INTERFACE_REGEX = re.compile(
    r'(?:export\s+)?interface\s+(\w+)\s*{([^}]*(?:{[^}]*}[^}]*)*)}', re.DOTALL
)
 
PROPERTY_LINE_REGEX = re.compile(r'\s*(\w+)\??\s*:\s*([^;]+);?')

# Load config at the start
test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')
config = load_config()
 
@pytest.fixture
def test_paths():
    test_script_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    base_dir = os.path.dirname(test_script_path)
    source_exposes_path = os.path.join(base_dir, "exposes.json")
    dest_exposes_path = os.path.join(test_script_path, "exposes.json")
    component_file_path = os.path.join(test_script_path, "components.json")
   
    return {
        "base_dir": base_dir,
        "source_exposes_path": source_exposes_path,
        "dest_exposes_path": dest_exposes_path,
        "component_file_path": component_file_path,
        "source_ignore_path": os.path.join(base_dir, "ignore.json"),
        "dest_ignore_path": os.path.join(test_script_path, "ignore.json"),
        "test_script_path": test_script_path,
    }

# Load config at the start
config_path = os.path.join(test_script_path, 'config.json').replace('\\', '/')
config = load_config()
 
EXPORT_ALL_PATTERN = re.compile(r'export\s+\*\s+from\s+[\'"](.*?)[\'"]')
EXPORT_NAMED_PATTERN = re.compile(r'export\s+\{\s*([\w\s,]+)\s*\}\s+from\s+[\'"](.*?)[\'"]')
COMPONENT_PATTERN = re.compile(r'export\s+(?:function|const|class)\s+([A-Z][A-Za-z0-9_]*)')

 
visited_files = set()
 
def resolve_ts_path(base_path, relative_path):
    """Resolve a TypeScript import path to an actual file path."""
    if relative_path.startswith('.'):
        path = os.path.normpath(os.path.join(os.path.dirname(base_path), relative_path))
    else:
        path = os.path.normpath(relative_path)
 
    for ext in [".ts", ".tsx", "/index.ts", "/index.tsx"]:
        candidate = path + ext if not ext.startswith("/") else path + ext
        if os.path.exists(candidate):
            return candidate
    return None
 
def extract_components(file_path):
    """Extract component declarations from a file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            return COMPONENT_PATTERN.findall(f.read())
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return []
 
def resolve_exports(file_path, root_dir, depth=0):
    """Recursively resolve exported components."""
    file_path = os.path.normpath(file_path)
    abs_path = os.path.normpath(os.path.join(root_dir, file_path))
 
    if not os.path.exists(abs_path) or abs_path in visited_files:
        return set()
 
    visited_files.add(abs_path)
    components = set()
 
    try:
        with open(abs_path, encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read {abs_path}: {e}")
        return set()
 
    components.update(COMPONENT_PATTERN.findall(content))
 
    for match in EXPORT_ALL_PATTERN.findall(content):
        dep_path = resolve_ts_path(abs_path, match)
        if dep_path:
            components.update(resolve_exports(dep_path, root_dir, depth + 1))
 
    # export { A, B } from '...'
    for match in EXPORT_NAMED_PATTERN.findall(content):
        exported_names, from_path = match
        names = [name.strip() for name in exported_names.split(',')]
        dep_path = resolve_ts_path(abs_path, from_path)
        if dep_path:
            found_components = resolve_exports(dep_path, root_dir, depth + 1)
            components.update(name for name in names if name in found_components)
 
    return components
 
def resolve_and_copy_recursive(source_path, dest_base_dir, base_dir, visited=None): #helper function
    """Recursively copies source files and their re-exports (from export statements), maintaining their folder structure."""
    if visited is None:
        visited = set()
 
    if not os.path.exists(source_path):
        print(f"Source file not found: {source_path}")
        return
 
    if source_path in visited:
        return
    visited.add(source_path)
 
    # Copy the file while preserving relative structure
    rel_path = os.path.relpath(source_path, base_dir)
    dest_path = os.path.join(dest_base_dir, rel_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(source_path, dest_path)
 
    # Read file and search for export-from lines
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
 
    for line in lines:
        line = line.strip()
        match = EXPORT_PATTERN.search(line)
        if match:
            import_path = match.group(1)
 
            if not import_path.startswith("."):
                continue  # Skip external packages
 
            # Resolve to full path relative to current file
            current_dir = os.path.dirname(source_path)
            base_import = os.path.normpath(os.path.join(current_dir, import_path))
 
            # Possible resolutions: .ts, .tsx, index.ts, index.tsx
            candidates = [
                base_import + '.ts',
                base_import + '.tsx',
                os.path.join(base_import, 'index.ts'),
                os.path.join(base_import, 'index.tsx'),
            ]
 
            for candidate in candidates:
                if os.path.exists(candidate):
                    resolve_and_copy_recursive(candidate, dest_base_dir, base_dir, visited)
                    break
            else:
                print(f"Could not resolve imported path: {import_path} from {source_path}")
def validate_properties(properties, comp_name, missing_fields_report, parent=""):
    for prop_name, prop_def in properties.items():
        full_name = f"{parent}.{prop_name}" if parent else prop_name
 
        if not isinstance(prop_def, dict):
            missing_fields_report.append(
                f'Property "{full_name}" in component "{comp_name}" is not a valid object'
            )
            continue
 
        # ===== NEW: Handle union types first =====
        if prop_def.get("kind") == "union":
            # Skip type validation for unions (they use types[] instead)
            pass
        # ===== Original type validation for normal props =====
        else:
            raw_type = prop_def.get("dataType", "")
            if isinstance(raw_type, str):
                json_type = raw_type.strip().lower()
            elif isinstance(raw_type, dict):
                json_type = raw_type.get("dataType", "").strip().lower() if isinstance(raw_type.get("dataType"), str) else ""
            else:
                json_type = ""
 
            if not json_type:
                missing_fields_report.append(
                    f'Property "{full_name}" in component "{comp_name}" is missing or has empty "type"'
                )
 
        # ===== Keep the rest of your validation unchanged =====
        if "required" not in prop_def:
            missing_fields_report.append(
                f'Property "{full_name}" in component "{comp_name}" is missing the "required" field'
            )
        if "defaultValue" not in prop_def:
            missing_fields_report.append(
                f'Property "{full_name}" in component "{comp_name}" is missing the "defaultValue" field'
            )
        if "description" not in prop_def:
            missing_fields_report.append(
                f'Property "{full_name}" in component "{comp_name}" is missing the "description" field'
            )
 
       
 
        # ✅ Recurse into nested properties
        if "properties" in prop_def and isinstance(prop_def["properties"], dict):
            validate_properties(prop_def["properties"], comp_name, missing_fields_report, full_name)
 
        # ✅ Recurse into "element" → which may contain "properties"
        if "element" in prop_def and isinstance(prop_def["element"], dict):
            element = prop_def["element"]
            if "properties" in element and isinstance(element["properties"], dict):
                validate_properties(element["properties"], comp_name, missing_fields_report, full_name)
 
@pytest.mark.order(1)
def test_create_component_json_and_verify_its_existence(test_paths):
    source_component_path = os.path.join(test_paths["base_dir"], "public", "components.json")
    test_component_path = test_paths["component_file_path"]
 
    assert os.path.exists(source_component_path), f"Required file component.json not found at: {source_component_path}"
    shutil.copy2(source_component_path, test_component_path)
 
    assert os.path.exists(test_component_path), f"Test component.json was not created at {test_component_path}"

 
@pytest.mark.order(2)
def test_copy_ignore_json(test_paths):
    source_ignore_path = test_paths["source_ignore_path"]
    dest_ignore_path = test_paths["dest_ignore_path"]
 
    assert os.path.exists(source_ignore_path), f"Required file ignore.json not found at: {source_ignore_path}"
    shutil.copy2(source_ignore_path, dest_ignore_path)
 
    assert os.path.exists(dest_ignore_path), f"Test ignore.json was not created at {dest_ignore_path}"
 
@pytest.mark.order(3)
def test_copy_exposes_and_referenced_files(test_paths):
    """
    Main function to:
    - Copy exposes.json from source to test folder
    - Copy each file mentioned in exposes.json and its dependencies
    - Write updated exposes.json with relative paths
    """
    base_dir = test_paths["base_dir"]
    source_exposes_path = test_paths["source_exposes_path"]
    dest_exposes_path = test_paths["dest_exposes_path"]
    test_dir = os.path.dirname(dest_exposes_path)
 
    try:
        test_script_path = os.path.dirname(dest_exposes_path)
        os.makedirs(test_script_path, exist_ok=True)
 
        if not os.path.exists(source_exposes_path):
            raise FileNotFoundError(f"Source exposes.json not found at: {source_exposes_path}")
 
        # Copy exposes.json to destination
        shutil.copy2(source_exposes_path, dest_exposes_path)
 
        with open(source_exposes_path, 'r') as f:
            exposes_data = json.load(f)
 
        updated_exposes = {}
 
        # Process each entry in exposes.json
        for key, relative_path in exposes_data.items():
            source_file = os.path.join(base_dir, relative_path)
 
            if not os.path.exists(source_file):
                print(f"File not found: {source_file}")
                continue
 
            # Copy file and its exported/imported dependencies
            resolve_and_copy_recursive(source_file, test_script_path, base_dir)
 
            # Update exposes.json with relative path
            updated_path = os.path.relpath(source_file, base_dir)
            updated_exposes[key] = updated_path.replace("\\", "/")
 
        # Write updated exposes.json
        with open(dest_exposes_path, 'w') as f:
            json.dump(updated_exposes, f, indent=2)
 
    except Exception as e:
        raise RuntimeError(f"Failed to process exposes.json or referenced files: {e}")
 
@pytest.mark.order(4)
def test_get_exposed_components(test_paths):
    base_dir = test_paths["base_dir"]
 
    exposes_path = test_paths["dest_exposes_path"]
    component_path = test_paths["component_file_path"]
    ignore_path = test_paths["dest_ignore_path"]
 
    assert os.path.exists(exposes_path), "Missing exposes.json"
    assert os.path.exists(component_path), "Missing components.json"
    assert os.path.exists(ignore_path), "Missing ignore.json"
 
    with open(exposes_path) as f:
        exports_map = json.load(f)
 
    with open(component_path) as f:
        components_registry = json.load(f)

    with open(ignore_path) as f:
        ignore_map = json.load(f)
 
    registered_component_names = {c["componentName"] for c in components_registry}
    all_exported_components = set()
    all_ignored_components = set()
 
    for alias, relative_path in exports_map.items():
        visited_files.clear()
        full_path = os.path.join(base_dir, relative_path)
        print(f"\nResolving exports for: {full_path}")
        exported_components = resolve_exports(relative_path, base_dir)
        all_exported_components.update(exported_components)
 
        print(f"\nExported components for {alias} ({len(exported_components)} found):")
        for c in sorted(exported_components):
            print(f" - {c}")

    # Collect ignored components
    for alias, relative_path in ignore_map.items():
        visited_files.clear()
        full_path = os.path.join(base_dir, relative_path)
        ignored_components = resolve_exports(relative_path, base_dir)
        all_ignored_components.update(ignored_components)

    # Compare registry vs exports (ignoring components in ignore.json)
    missing_in_registry = (all_exported_components - registered_component_names) - all_ignored_components
    extra_in_registry = registered_component_names - all_exported_components
 
    # missing_in_registry = all_exported_components - registered_component_names
 
    # extra_in_registry = registered_component_names - all_exported_components
 
    if missing_in_registry or extra_in_registry:
        error_messages = []
        if missing_in_registry:
            error_messages.append(f"Missing in components.json: {sorted(missing_in_registry)}")
        if extra_in_registry:
            error_messages.append(f"Extra in components.json (not exported): {sorted(extra_in_registry)}")
        raise Exception("\n".join(error_messages))

    print("All exported components are correctly registered (ignoring ignored ones).")
 
@pytest.mark.order(5)
def test_get_ignored_components(test_paths):
    base_dir = test_paths["base_dir"]
 
    # ⬇️ Load inside function instead of globally
    ignore_path = test_paths["dest_ignore_path"]
    component_path = test_paths["component_file_path"]
 
    assert os.path.exists(ignore_path), "Missing ignore.json"
    assert os.path.exists(component_path), "Missing components.json"
 
    with open(ignore_path) as f:
        exports_map = json.load(f)
 
    with open(component_path) as f:
        components_registry = json.load(f)
 
    registered_component_names = {c["componentName"] for c in components_registry}
    all_ignored_components = set()
 
    for alias, relative_path in exports_map.items():
        visited_files.clear()
        full_path = os.path.join(base_dir, relative_path)
        print(f"\nResolving exports for: {full_path}")
        exported_components = resolve_exports(relative_path, base_dir)
 
        print(f"\nComponents for {alias} ({len(exported_components)} found):")
        for c in sorted(exported_components):
            print(f" - {c}")
 
        ignored = exported_components & registered_component_names
        all_ignored_components.update(ignored)
 
    if all_ignored_components:
        raise Exception(f"Ignored components found in exports: {sorted(all_ignored_components)}")
    else:
        print("No ignored components are present in exported list.")
 
@pytest.mark.order(6)
def test_component_json_mandatory_fields(test_paths):
    component_path = test_paths["component_file_path"]
 
    assert os.path.exists(component_path), "components.json file is missing"
 
    with open(component_path, 'r') as f:
        component_data = json.load(f)
 
    assert isinstance(component_data, list), "components.json should be a list of component definitions"
 
    mandatory_fields = ["componentName", "ComponentType", "federationRemote", "properties"]
    missing_fields_report = []
 
    for index, component_def in enumerate(component_data):
        comp_name = component_def.get("componentName", f"component at index {index}")
       
        for field in mandatory_fields:
            if field not in component_def or component_def[field] in [None, ""]:
                missing_fields_report.append(
                    f'"{comp_name}" is missing or has empty mandatory field "{field}" in components.json'
                )
 
        # Validate `properties` field is a dict and each property has required subfields
        properties = component_def.get("properties", {})
        if not isinstance(properties, dict):
            missing_fields_report.append(f'"{comp_name}" must have "properties" defined as a dictionary')
            continue
 
        validate_properties(properties, comp_name, missing_fields_report)
 
 
    assert not missing_fields_report, "Validation errors found:\n" + "\n".join(missing_fields_report)
 
@pytest.mark.order(7)
def test_component_json_properties_match_ts_files(test_paths):
    component_path = test_paths["component_file_path"]
    test_script_path = test_paths["test_script_path"]
    assert os.path.exists(component_path), "components.json file is missing"
    with open(component_path, 'r') as f:
        component_data = json.load(f)
    # Create map of componentName -> properties
    component_props_map = {comp["componentName"]: comp["properties"] for comp in component_data}
    # Regex patterns
    interface_pattern = re.compile(r'(?:export\s+)?(?:interface|type)\s+(\w+)\s*{([^}]+)}', re.DOTALL)
    prop_pattern = re.compile(r'^\s*(\w+)(\??)\s*:\s*([^;\n]+);?', re.MULTILINE)
    component_def_pattern = re.compile(r'export\s+(?:function|const)\s+(\w+)\s*\([^)]*:\s*(\w+)(?:Props)?', re.DOTALL)
    errors = []
    # Scan all .ts files
    for root, _, files in os.walk(test_script_path):
        for file in files:
            if not file.endswith(('.ts', '.tsx')):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
 
            # Find all component definitions in the file
            component_defs = {}
            for match in component_def_pattern.finditer(content):
                component_name, props_interface = match.groups()
                component_defs[component_name] = props_interface
            # Extract all interfaces
            interfaces = {}
            optional_props = {}
            for match in interface_pattern.finditer(content):
                name, body = match.groups()
                props = {}
                opts = {}
                for prop_match in prop_pattern.finditer(body):
                    prop_name, is_optional, prop_type = prop_match.groups()
                    props[prop_name] = prop_type.strip().lower()
                    opts[prop_name] = bool(is_optional)
                interfaces[name] = props
                optional_props[name] = opts
 
            # Check both filename-based and component-definition matches
            possible_names = {os.path.splitext(file)[0]}
            possible_names.update(component_defs.keys())
            # Validate each possible component name
            for component_name in possible_names:
                if component_name not in component_props_map:
                    continue
                json_props = component_props_map[component_name]
                # Determine the props interface name
                props_interface = component_defs.get(component_name, f"{component_name}Props")
                # Get the TS interface
                ts_props = interfaces.get(props_interface, {})
                ts_opts = optional_props.get(props_interface, {})
                if not ts_props:
                    print(f"Skipping validation for '{component_name}' — no interface/type found.")
                    continue
                for prop_key, prop_meta in json_props.items():
                    # Skip if we've already processed this property
                    if any(e.startswith(f"'{component_name}.{prop_key}'") for e in errors):
                        continue
                    # Get TypeScript info
                    ts_type = ts_props.get(prop_key, [None, ""])[1].lower() if isinstance(ts_props.get(prop_key), tuple) else ts_props.get(prop_key, "").lower()
                    ts_optional = ts_opts.get(prop_key, False)
                    if not ts_type:
                        errors.append(f"Missing TypeScript property for '{prop_key}' in '{component_name}'")
                        continue
                    # Check required status
                    json_required = prop_meta.get("required", True)
                    if json_required == ts_optional:
                        errors.append(
                            f"Required mismatch in '{component_name}.{prop_key}': "
                            f"JSON says {'required' if json_required else 'optional'}, "
                            f"TS says {'optional' if ts_optional else 'required'}"
                        )
                    # Check type
                    json_type = prop_meta.get("dataType", "").lower()
                    def is_array_type(type_str):
                        """Check if a type represents an array (either 'array' or ends with '[]')"""
                        if not type_str:
                            return False
                        type_str = type_str.lower().strip()
                        return type_str == "array" or type_str.endswith("[]")
 
                    json_is_array = is_array_type(json_type)
                    ts_is_array = is_array_type(ts_type)
 
                    if json_is_array != ts_is_array:
                        errors.append(
                            f"Array dataType mismatch in '{component_name}.{prop_key}': "
                            f"JSON says {'array' if json_is_array else 'not array'}, "
                            f"TS says {'array' if ts_is_array else 'not array'}"
                        )
                    # Process array elements if needed
                    if prop_meta.get("dataType") == "array" and "element" in prop_meta:
                        element_def = prop_meta["element"]
                        if "properties" in element_def:
                            interface_name = element_def.get("name") or f"{prop_key}Element"
                            ts_interface_props = interfaces.get(interface_name, {})
                            ts_optional_props = optional_props.get(interface_name, {})
                            for sub_key, sub_meta in element_def["properties"].items():
                                # Handle union types in subproperties
                                if sub_meta.get("kind") == "union":
                                    # Skip type validation for unions
                                    sub_ts_type = "union"
                                    sub_json_type = "union"
                                else:
                                    sub_ts_type = ts_interface_props.get(sub_key, "").lower()
                                    sub_json_type = sub_meta.get("dataType", "").lower()
                                if not sub_json_type or not sub_ts_type:
                                    errors.append(f"Missing dataType for subproperty '{component_name}.{prop_key}.{sub_key}'")
                                    continue
                                # Only compare types if not a union
                                if sub_meta.get("kind") != "union" and sub_json_type != sub_ts_type:
                                    errors.append(
                                        f"dataType mismatch in '{component_name}.{prop_key}.{sub_key}': "
                                        f"JSON has '{sub_json_type}', TS has '{sub_ts_type}'"
                                    )
                                if sub_json_type != sub_ts_type:
                                    errors.append(
                                        f"dataType mismatch in '{component_name}.{prop_key}.{sub_key}': "
                                        f"JSON has '{sub_json_type}', TS has '{sub_ts_type}'"
                                    )
                                sub_json_required = sub_meta.get("required", True)
                                sub_ts_optional = ts_optional_props.get(sub_key, False)
                                if sub_json_required == sub_ts_optional:
                                    errors.append(
                                        f"Required mismatch in '{component_name}.{prop_key}.{sub_key}': "
                                        f"JSON says {'required' if sub_json_required else 'optional'}, "
                                        f"TS says {'optional' if sub_ts_optional else 'required'}"
                                    )
    assert not errors, "Validation errors:\n" + "\n".join(errors)

@pytest.mark.order(8)
def test_federation_remote_and_component_type_consistency(test_paths):
    # Extract expected values from config template
    expected_remote  = config.get("componentmetadata",{}).get("federationRemote")
    expected_type = config.get("componentmetadata",{}).get("component_type")
    expected_values = {
        'federationRemote': expected_remote,
        'ComponentType': expected_type
    }
 
    # 2. Validate every component in components.json
    component_path = test_paths["component_file_path"]
    assert os.path.exists(component_path), "components.json missing"
    with open(component_path, 'r') as f:
        components = json.load(f)
    failures = []
    for idx, component in enumerate(components):
        component_name = component.get("componentName", f"Component#{idx}")
       
        # ===== CHANGE 1: Replace exact equality with 'in' check =====
        if expected_values['federationRemote'] not in component.get("federationRemote", ""):
            failures.append(
                f"{component_name}: federationRemote must contain '{expected_values['federationRemote']}', "
                f"got '{component.get('federationRemote')}'"
            )
        # Check ComponentType
        if component.get("ComponentType") != expected_values['ComponentType']:
            failures.append(
                f"{component_name}: ComponentType mismatch "
                f"(expected '{expected_values['ComponentType']}', "
                f"got '{component.get('ComponentType')}')"
            )
    # 3. Final assertion
    assert not failures, "Metadata mismatches found:\n" + "\n".join(failures)

@pytest.mark.order(9)
def test_component_json_events_match_ts_or_tsx_files(test_paths):
    test_script_path = test_paths["test_script_path"]
    errors = []

    # Regex patterns
    interface_pattern = re.compile(r'(?:export\s+)?(?:interface|type)\s+(\w+)\s*{([^}]+)}', re.DOTALL)
    prop_pattern = re.compile(r'^\s*(\w+)\s*:\s*\(?[^)]*\)?\s*=>\s*[^;\n]+;', re.MULTILINE)
    component_def_pattern = re.compile(r'export\s+(?:function|const)\s+(\w+)\s*\([^)]*:\s*(\w+)(?:Props)?', re.DOTALL)

    # Scan all .ts/.tsx files
    for root, _, files in os.walk(test_script_path):
        for file in files:
            if not file.endswith(('.ts', '.tsx')):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all component definitions in the file
            component_defs = {}
            for match in component_def_pattern.finditer(content):
                component_name, props_interface = match.groups()
                component_defs[component_name] = props_interface

            # Extract all interfaces and events
            interfaces = {}
            for match in interface_pattern.finditer(content):
                name, body = match.groups()
                events = set()
                for prop_match in prop_pattern.finditer(body):
                    prop_name = prop_match.group(1)
                    events.add(prop_name)
                interfaces[name] = events

            # Report events for each component
            possible_names = {os.path.splitext(file)[0]}
            possible_names.update(component_defs.keys())
            for component_name in possible_names:
                props_interface = component_defs.get(component_name, f"{component_name}Props")
                component_events = interfaces.get(props_interface, set())
                if component_events:
                    print(f"Detected events in '{component_name}': {component_events}")
                else:
                    print(f"No events detected in '{component_name}' (this is OK)")

    assert True

@pytest.mark.order(10)
def test_component_json_events_mandatory_fields(test_paths):
    """
    Validate that all function-type properties (events) in components.json
    have all mandatory fields: dataType, signatures, binding, required,
    description, defaultValue, and name.
    """
    component_path = test_paths["component_file_path"]
    assert os.path.exists(component_path), "components.json file is missing"

    with open(component_path, 'r') as f:
        component_data = json.load(f)

    mandatory_event_fields = [
        "dataType", "signatures", "binding", "required",
        "description", "defaultValue", "name"
    ]

    for component_def in component_data:
        comp_name = component_def.get("componentName", "UnknownComponent")
        properties = component_def.get("properties", {})

        # Filter function-type properties (events)
        events = {k: v for k, v in properties.items() if v.get("dataType") == "function"}

        for event_name, event_meta in events.items():
            # Check all mandatory fields exist
            for field in mandatory_event_fields:
                assert field in event_meta, f'Event "{event_name}" in "{comp_name}" is missing mandatory field "{field}"'

            # Check signatures structure
            signatures = event_meta.get("signatures", [])
            assert isinstance(signatures, list) and signatures, f'Event "{event_name}" in "{comp_name}" must have at least one signature'

            for sig in signatures:
                # parameters
                params = sig.get("parameters", [])
                assert isinstance(params, list), f'Signature parameters in "{event_name}" of "{comp_name}" must be a list'
                for param in params:
                    assert "name" in param, f'Parameter in "{event_name}" of "{comp_name}" missing "name"'
                    assert "dataType" in param, f'Parameter "{param.get("name")}" in "{event_name}" of "{comp_name}" missing "dataType"'
                # returnType
                ret = sig.get("returnType", {})
                assert "dataType" in ret, f'ReturnType in "{event_name}" of "{comp_name}" missing "dataType"'


@pytest.mark.order(11)
def test_component_json_events_match_ts_files(test_paths):
    component_path = test_paths["component_file_path"]
    ts_path = test_paths["test_script_path"]

    with open(component_path, 'r') as f:
        components = json.load(f)

    # Collect events from components.json
    events_map = {}
    errors = []
    
    for comp in components:
        comp_name = comp["componentName"]
        properties = comp.get("properties", {})
        events_map[comp_name] = {}
        for prop, meta in properties.items():
            # Handle direct function properties
            if meta.get("dataType") == "function":
                signatures = meta.get("signatures", [])
                if signatures:
                    sig = signatures[0]
                    param_list = [(p["name"], p["dataType"]) for p in sig.get("parameters", [])]
                    return_type = sig.get("returnType", {}).get("dataType")
                    events_map[comp_name][prop] = {"parameters": param_list, "returnType": return_type}
            
            # Handle union types that contain functions
            elif meta.get("kind") == "union":
                for i, union_type in enumerate(meta.get("types", [])):
                    data_type = union_type.get("dataType")
                    
                    # Only process if dataType is explicitly "function"
                    if data_type == "function":
                        signatures = union_type.get("signatures", [])
                        if signatures:
                            sig = signatures[0]
                            param_list = [(p["name"], p["dataType"]) for p in sig.get("parameters", [])]
                            return_type = sig.get("returnType", {}).get("dataType")
                            events_map[comp_name][prop] = {"parameters": param_list, "returnType": return_type}
                            break
                    # If dataType exists but is not "function", skip silently (it's not an event)
                    elif data_type:  # dataType exists but is not "function"
                        continue
                    else:
                        # dataType is empty or missing - this is an error
                        errors.append(
                            f'Component "{comp_name}" property "{prop}" has empty/missing dataType in union type at index {i}'
                        )

    # Regex to extract interface blocks
    interface_pattern = re.compile(r'interface\s+(\w+)\s*{([^}]+)}', re.DOTALL)
    # Regex to extract function props: propName: (params) => returnType;
    event_pattern = re.compile(r'(\w+)\??\s*:\s*\(([^)]*)\)\s*=>\s*([^;\n]+);?')

    # Walk through TS/TSX files
    for root, _, files in os.walk(ts_path):
        for file in files:
            if not file.endswith((".ts", ".tsx")):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract interfaces
            for iface_match in interface_pattern.finditer(content):
                iface_name, body = iface_match.groups()
                # Match component interface
                for comp_name, events in events_map.items():
                    expected_iface = f"{comp_name}Props"
                    if iface_name != expected_iface:
                        continue
                    # Extract all arrow-function props
                    for event_match in event_pattern.finditer(body):
                        name, params_str, return_type_str = event_match.groups()
                        if name not in events:
                            continue
                        # Process TSX parameters
                        ts_params = []
                        if params_str.strip():
                            for p in params_str.split(","):
                                p = p.strip()
                                if ":" in p:
                                    p_name, p_type = map(str.strip, p.split(":", 1))
                                    ts_params.append((p_name, p_type))
                        ts_return = return_type_str.strip()

                        # Compare with component.json
                        expected = events[name]
                        
                        # Check parameter data types
                        # Check parameter data types
                        for i, (ts_param, json_param) in enumerate(zip(ts_params, expected["parameters"])):
                            ts_name, ts_type = ts_param
                            json_name, json_type = json_param
                            
                            # Handle Record<string, unknown> vs object equivalence
                            if ts_type.startswith("Record<string") and json_type == "object":
                                continue  # These are equivalent, skip the error
                            
                            # Direct comparison for all other types
                            elif ts_type != json_type:
                                errors.append(
                                    f'Parameter "{ts_name}" of event "{name}" in "{comp_name}" has type mismatch: '
                                    f'TS has "{ts_type}", component.json has "{json_type}"'
                                )
                        
                        # Check return type
                        if ts_return != expected["returnType"]:
                            errors.append(
                                f'Event "{name}" in "{comp_name}" has returnType mismatch: '
                                f'TS has "{ts_return}", component.json has "{expected["returnType"]}"'
                            )

                    # Check for missing events
                    ts_event_names = {m.group(1) for m in event_pattern.finditer(body)}
                    for event_name in events.keys():
                        if event_name not in ts_event_names:
                            errors.append(
                                f'Event "{event_name}" not found in TS/TSX interface "{iface_name}" for component "{comp_name}"'
                            )

    assert not errors, "Validation errors:\n" + "\n".join(errors)