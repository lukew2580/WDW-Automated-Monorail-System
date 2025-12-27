# WDW Monorail Sensors Ruby Gem
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'wdw_sensors/version'

Gem::Specification.new do |spec|
  spec.name          = "wdw-sensors"
  spec.version       = WDW::VERSION
  spec.authors       = ["WDW Monorail System"]
  spec.email         = ["contact@wdw-monorail.com"]
  
  spec.summary       = "WDW Monorail Sensors Library"
  spec.description   = "A Ruby library for interacting with sensors in the WDW Monorail System."
  spec.homepage      = "https://github.com/wdw-monorail/wdw-sensors"
  spec.license       = "MIT"
  
  spec.files         = `git ls-files -z`.split("\x0")
  spec.bindir        = "bin"
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]
  
  spec.add_development_dependency "bundler", "~> 2.0"
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.0"
end
