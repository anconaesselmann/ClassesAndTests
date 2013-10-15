Classes and Tests (beta) 
A file creator and test runner for PSR-0 name-spaced class and test files (Templates supplied are for php and phpUnit)

Add to user key bindings to activate vintage mode key bindings:

    {
        "keys": [",", "n"],
        "command": "classes_and_tests",
        "context":
            [
                {"key": "setting.vintage_ctrl_keys"},
                {"key": "setting.command_mode"}
            ]
    },
    {
        "keys": [",", "t"],
        "command": "toggle_source_test",
        "context":
            [
                {"key": "setting.vintage_ctrl_keys"},
                {"key": "setting.command_mode"}
            ]
    },
    {
        "keys": [",", "r"],
        "command": "run_php_unit_tests",
        "context":
            [
                {"key": "setting.vintage_ctrl_keys"},
                {"key": "setting.command_mode"}
            ]
    },
    {
        "keys": [",", ",", "r"],
        "command": "run_php_unit_tests", "args": {"run_test_suite": true},
        "context":
            [
                {"key": "setting.vintage_ctrl_keys"},
                {"key": "setting.command_mode"}
            ]
    },
    {
        "keys": [",", "r"],
        "command": "hide_panel", "args": {"cancel": true},
        "context":
            [
                {"key": "setting.vintage_ctrl_keys"},
                {"key": "setting.command_mode"},
                { "key": "panel_visible", "operator": "equal", "operand": true }/*,
                { "key": "setting.php_unit_output_panel", "operator": "equal"}*/
            ]
    }



    Known issues:
        Currently only key-bindings for Mac exist.