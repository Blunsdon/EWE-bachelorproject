package com.example.controllockbt

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.content.Context
import android.content.Intent
import android.location.LocationManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import androidx.activity.viewModels
import androidx.core.location.LocationManagerCompat
import androidx.core.app.ActivityCompat
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.Navigation
import com.example.controllockbt.activities.Login.LoginFragViewModel
import com.example.controllockbt.activities.Logout.LogoutFragModelFactory
import com.example.controllockbt.activities.Logout.LogoutFragViewModel
import com.example.controllockbt.repository.Repository


class MainActivity : AppCompatActivity() {

    //add view model
    private lateinit var tokenmodel: LogOut
    private lateinit var viewModel: LogoutFragViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tokenmodel = ViewModelProvider(this).get(LogOut::class.java)

        val lm = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        if (!LocationManagerCompat.isLocationEnabled(lm)) {
            // Start Location Settings Activity, you should explain to the user why he need to enable location before.
            startActivity(Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS))
        }
        ActivityCompat.requestPermissions(
            this, arrayOf(
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_BACKGROUND_LOCATION,
                Manifest.permission.BLUETOOTH_SCAN,
                Manifest.permission.BLUETOOTH,
                Manifest.permission.BLUETOOTH_ADMIN,
                Manifest.permission.BLUETOOTH_CONNECT
            ), 0
        )
    }

    override fun onDestroy() {
        super.onDestroy()
        val token = tokenmodel.getToken()
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = LogoutFragModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(LogoutFragViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(token.toString())
        viewModel.pushPost(tokenString)
    }
}