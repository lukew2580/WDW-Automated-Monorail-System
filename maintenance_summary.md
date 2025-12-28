# WDW Monorail Maintenance Report

**Generated:** 2025-12-28 07:07:29

**Status:** ✅ Success

## Task Results

### ⚠️ Git Status Check

**Status:** warning

**Message:** Local changes detected

**Details:** M maintenance.log

---

### ✅ Dependency Checks

**Status:** success

**Message:** Dependabot configured and active

**Dependencies Checked:** 49

---

### ❌ Test Execution

**Status:** error

**Message:** Some tests failed

**Output:** wdw_sensors (unittest.loader._FailedTest.wdw_sensors) ... ERROR

======================================================================
ERROR: wdw_sensors (unittest.loader._FailedTest.wdw_sensors)
----------------------------------------------------------------------
ImportError: Failed to import test module: wdw_sensors
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/unittest/loader.py", line 427, in _find_test_path
    package = self._get_module_from_name(name)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/unittest/loader.py", line 337, in _get_module_from_name
    __import__(name)
  File "/home/workspace/WDW-Automated-Monorail-System/wdw_sensors/__init__.py", line 4, in <module>
    from .dht22 import DHT22
  File "/home/workspace/WDW-Automated-Monorail-System/wdw_sensors/dht22.py", line 1, in <module>
    import Adafruit_DHT
ModuleNotFoundError: No module named 'Adafruit_DHT'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)


---

### ⚠️ Security Scan

**Status:** warning

**Message:** Security issues detected

**Issues:** ['Missing security files: README.md']

---

### ✅ Report Generation

**Status:** success

**Message:** Report generated successfully

**Report Path:** /home/workspace/WDW-Automated-Monorail-System/maintenance_report.json

---


**Duration:** 0.0 seconds
