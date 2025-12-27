// Java Example
// Demonstrates using the Java library to read sensor data.

import com.wdw.sensors.DHT22;
import com.wdw.sensors.MPU6050;

public class JavaExample {
    public static void main(String[] args) throws InterruptedException {
        DHT22 dht22 = new DHT22(4);
        MPU6050 mpu6050 = new MPU6050();
        
        System.out.println("Java Example");
        System.out.println("Press Ctrl+C to exit");
        
        try {
            while (true) {
                // Read DHT22
                DHT22.Data dhtData = dht22.read();
                System.out.println("DHT22: Temperature=" + dhtData.temperature + "°C, Humidity=" + dhtData.humidity + "%");
                
                // Read MPU6050
                MPU6050.Data mpuData = mpu6050.read();
                System.out.println("MPU6050: Accel X=" + mpuData.accel.x + ", Gyro X=" + mpuData.gyro.x);
                
                Thread.sleep(2000);
            }
        } catch (InterruptedException e) {
            System.out.println("Exiting...");
        }
    }
}
