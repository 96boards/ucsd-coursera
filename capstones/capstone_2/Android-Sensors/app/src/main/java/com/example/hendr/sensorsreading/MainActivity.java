package com.example.hendr.sensorsreading;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.hardware.*;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity implements SensorEventListener{

    private SensorManager mSensorManager;
    private Sensor mMagneticSensor;
    private Sensor mAccelerometer;
    private Sensor mTemperature;
    private Sensor mLight;

    TextView sensor1Text; float magneticFieldReading;
    TextView sensor2Text; float acclerationReadingX, acclerationReadingY, acclerationReadingZ;
    TextView sensor3Text; float temperatureReading;
    TextView sensor4Text; float lightReading;
    TextView sensor5Text; //float magneticFieldReading;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /*
        Button button = (Button) findViewById(R.id.button1);
        button.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, Main2Activity.class);
                startActivity(intent);
            }
        });
        */

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        sensor1Text = (TextView)findViewById(R.id.sensor1);
        sensor2Text = (TextView)findViewById(R.id.sensor2);
        sensor3Text = (TextView)findViewById(R.id.sensor3);
        sensor4Text = (TextView)findViewById(R.id.sensor4);
        sensor5Text = (TextView)findViewById(R.id.sensor5);


        if (mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD) != null){
            mMagneticSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
            mSensorManager.registerListener(this, mMagneticSensor , SensorManager.SENSOR_DELAY_NORMAL);
        }
        else {
            sensor1Text.setText("Failed to get the magnetic sensor");
        }

        if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null){
            mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            mSensorManager.registerListener(this, mAccelerometer , SensorManager.SENSOR_DELAY_NORMAL);
        }
        else {
            sensor2Text.setText("Failed to get the accelerometer");
        }

        if (mSensorManager.getDefaultSensor(Sensor.TYPE_AMBIENT_TEMPERATURE) != null){
            mTemperature = mSensorManager.getDefaultSensor(Sensor.TYPE_AMBIENT_TEMPERATURE);
            mSensorManager.registerListener(this, mTemperature , SensorManager.SENSOR_DELAY_NORMAL);
        }
        else {
            sensor3Text.setText("Failed to get the temperature");
        }

        if (mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT) != null){
            mLight = mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
            mSensorManager.registerListener(this, mLight , SensorManager.SENSOR_DELAY_NORMAL);
        }
        else {
            sensor4Text.setText("Failed to get the light sensor");
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        if (event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
            magneticFieldReading = event.values[0];
            sensor1Text.setText("Magnetic Field : " + String.valueOf(magneticFieldReading));
        }

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            acclerationReadingX = event.values[0];
            acclerationReadingY = event.values[1];
            acclerationReadingZ = event.values[2];
            sensor2Text.setText("Acceleration : X:" + String.valueOf(acclerationReadingX)
            + " Y:" + String.valueOf(acclerationReadingY) + " Z:" + String.valueOf(acclerationReadingZ)
            );
        }

        if (event.sensor.getType() == Sensor.TYPE_AMBIENT_TEMPERATURE) {
            temperatureReading = event.values[0];
            sensor3Text.setText(String.valueOf(temperatureReading));
        }

        if (event.sensor.getType() == Sensor.TYPE_LIGHT) {
            lightReading = event.values[0];
            sensor4Text.setText("Light: " + String.valueOf(lightReading));
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    public void buttonClick(View v){
        Intent intent = new Intent(MainActivity.this, Main2Activity.class);
        startActivity(intent);
    }
}
