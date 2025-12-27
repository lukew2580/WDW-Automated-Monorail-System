# Makefile for WDW Monorail Sensors Library

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -I.
CXXFLAGS = -Wall -Wextra -I.
LDFLAGS = -lpigpio

# C Library
LIB_C = libwdw_sensors.a
SRC_C = wdw_sensors.c
OBJ_C = wdw_sensors.o

# C++ Library
LIB_CPP = libwdw_sensors_cpp.a
SRC_CPP = wdw_sensors.cpp
OBJ_CPP = wdw_sensors.o

# Examples
EXAMPLES = dht22_example mpu6050_example

all: $(LIB_C) $(LIB_CPP) $(EXAMPLES)

$(LIB_C): $(OBJ_C)
	$(AR) rcs $@ $^

$(OBJ_C): $(SRC_C)
	$(CC) $(CFLAGS) -c $< -o $@

$(LIB_CPP): $(OBJ_CPP)
	$(AR) rcs $@ $^

$(OBJ_CPP): $(SRC_CPP)
	$(CXX) $(CXXFLAGS) -c $< -o $@

dht22_example: dht22_example.c $(LIB_C)
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) -L. -lwdw_sensors

mpu6050_example: mpu6050_example.c $(LIB_C)
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) -L. -lwdw_sensors

clean:
	rm -f $(OBJ_C) $(OBJ_CPP) $(LIB_C) $(LIB_CPP) $(EXAMPLES)

.PHONY: all clean
