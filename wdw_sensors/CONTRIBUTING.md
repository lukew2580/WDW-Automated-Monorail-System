# Contributing to WDW Monorail Sensors

We welcome contributions! Here’s how you can help:

## Reporting Issues
- Use GitHub Issues to report bugs or request features.
- Include:
  - A clear description of the issue
  - Steps to reproduce
  - Expected and actual behavior
  - Screenshots or logs if applicable

## Development Setup

### Python
```bash
git clone https://github.com/wdw-monorail/wdw-sensors.git
cd wdw-sensors
pip install -e .
```

### Java
```bash
cd wdw-sensors-java
mvn install
```

### Ruby
```bash
cd wdw-sensors-ruby
bundle install
```

### C/C++
```bash
cd wdw-sensors-c
make
```

## Pull Requests
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests for your changes.
4. Ensure all tests pass.
5. Submit a pull request with a clear description of your changes.

## Testing
- Write unit tests for new features.
- Ensure all tests pass before submitting a PR.

## License
By contributing, you agree to the terms of the [MIT License](LICENSE).
