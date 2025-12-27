# Ruby Example
# Demonstrates using the Ruby library to read sensor data.

require 'wdw_sensors'

dht22 = WDW::DHT22.new(pin: 4)
mpu6050 = WDW::MPU6050.new

puts "Ruby Example"
puts "Press Ctrl+C to exit"

begin
  loop do
    # Read DHT22
    dht_data = dht22.read
    puts "DHT22: Temperature=#{dht_data[:temperature]}°C, Humidity=#{dht_data[:humidity]}%"
    
    # Read MPU6050
    mpu_data = mpu6050.read
    puts "MPU6050: Accel=#{mpu_data[:accel]}, Gyro=#{mpu_data[:gyro]}"
    
    sleep 2
  end
rescue Interrupt
  puts "Exiting..."
end
