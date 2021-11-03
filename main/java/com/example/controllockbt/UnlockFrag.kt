package com.example.controllockbt

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothSocket
import android.content.Context
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ProgressBar
import android.widget.TextView
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.Navigation
import androidx.navigation.fragment.findNavController
import com.example.controllockbt.activities.SendLog.SendLogModelFactory
import com.example.controllockbt.activities.SendLog.SendLogViewModel
import com.example.controllockbt.model.Facility
import com.example.controllockbt.model.PostSendLog
import com.example.controllockbt.repository.Repository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException
import java.time.Instant
import java.time.format.DateTimeFormatter
import java.util.*

class UnlockFrag : Fragment() {

    //Bundle var's
    private lateinit var Token: String
    private lateinit var UserEmail: String
    private lateinit var FacName: String
    private lateinit var MacAdress: String

    //Bluetooth var's
    private var mMyUUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
    private var mBluetoothSocket: BluetoothSocket? = null
    private lateinit var mBluetoothAdapter: BluetoothAdapter
    private var mIsConnected: Boolean = false

    // restAPI variables
    private lateinit var viewModel: SendLogViewModel
    private lateinit var keyString: String

    //temp var's till restAPI is updated
    private var temp_companyString: String = "temp comp"
    private var temp_facLocation: String = "temp location"
    private var temp_userName: String = "temp user"

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_unlock, container, false)

        //Get arguments
        val args = this.arguments
        //get a specific data entry in the bundle
        Token = args?.get("Token").toString()
        UserEmail = args?.get("UserEmail").toString()
        FacName = args?.get("FacName").toString()
        MacAdress = args?.get("MacAdress").toString()

        sendLog()

        Log.d("uf_bundleInfo", "Token: " + Token)
        Log.d("uf_bundleInfo", "UserEmail: " + UserEmail)
        Log.d("uf_bundleInfo", "FacName: " + FacName)
        Log.d("uf_bundleInfo", "MacAdress: " + MacAdress)

        return view
    }

    private fun sendLog(){
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = SendLogModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(SendLogViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(Token)

        // TODO: change to correct variables after restAPI is fixed
        var fac: List<Facility> = listOf(Facility(FacName))
        var log: List<com.example.controllockbt.model.Log> = listOf(com.example.controllockbt.model.Log(temp_userName, temp_companyString, DateTimeFormatter.ISO_INSTANT.format(
            Instant.now()), UserEmail, FacName, temp_facLocation))
        val myPost = PostSendLog(fac, log,"")

        viewModel.pushPost(tokenString, myPost)
        //read response
        Log.d("restAPI", "sending log")
        viewModel.myResponse.observe(viewLifecycleOwner, { response ->
            if (response.isSuccessful) {
                //got a response
                Log.d("restAPI: Response msg", response.message().toString())
                keyString = response.body()?.key.toString()
                Log.d("restAPI: Response code", response.code().toString())

                //response okay -> launch coroutines

                    connectBt()

            } else {
                //no response
                Log.d("restAPI: Response-error", response.message().toString())
                Log.d("restAPI: Response-error", response.code().toString())

                // TODO: bad response do something!
            }
        })
    }

    private fun editMainThread(status: String) {

            setNewStatus(status)

    }

    private fun setNewStatus(status: String){
        val progressBar: ProgressBar? = view?.findViewById(R.id.progressBarUnlock)
        val textCode: TextView? = view?.findViewById(R.id.textViewUnlock)
        if(status == "done"){
            var bundle = Bundle()
            bundle.putString("Token", Token)
            bundle.putString("UserEmail", UserEmail)
            bundle.putString("FacName", FacName)
            view?.let { Navigation.findNavController(it).navigate(R.id.action_unlockFrag_to_successFrag, bundle) }
        } else {
            progressBar?.visibility = View.VISIBLE
            textCode?.text = "Unlocking door!"
        }
    }

    private fun sendCommand(input: String, view: View): Boolean {
        Log.d("SCCode", keyString)
        if(mBluetoothSocket != null){
            Log.d("sendCommand", "Socket not null")
            try {
                if(mBluetoothSocket!!.isConnected == true) {
                    Log.d("sendCommand", "Sending msg: " + keyString)
                    mBluetoothSocket!!.outputStream.write(keyString.toByteArray())
                }
            } catch (e: IOException) {
                Log.d("sendCommand error", e.toString())
            }
            try {
                if(mBluetoothSocket!!.isConnected == true) {
                    mBluetoothSocket!!.close()
                    mBluetoothSocket = null
                    mIsConnected = false
                }
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }
        return true
    }

    private fun connectBt() {
        editMainThread("start")
        try {
            if (mBluetoothSocket == null || !mIsConnected) {
                val bluetoothManager =
                    context?.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
                bluetoothManager.adapter.cancelDiscovery()
                mBluetoothAdapter = bluetoothManager.adapter
                val device: BluetoothDevice = mBluetoothAdapter.getRemoteDevice(MacAdress)
                kotlin.runCatching {
                    mBluetoothSocket = device.createInsecureRfcommSocketToServiceRecord(mMyUUID)
                }

                try{
                    mBluetoothSocket!!.connect()
                    Log.d("connectBt", "connected")
                } catch (e: IOException){
                    Log.d("connectBt", "error: couldn't connect")
                }
                mIsConnected = true
                Log.d("connectBt", "success: BtSocket created")
                if(view?.let { sendCommand("42", it) } == true){
                    editMainThread("done")
                }
            } else {
                Log.d("connectBt", "error: BtSocket not null")
            }
        } catch (e: IOException) {
            Log.d("connectBt", "error: " + e.toString())
            mIsConnected = false
            e.printStackTrace()
        }
    }

    override fun onDestroy() {
        mBluetoothSocket?.close()
        super.onDestroy()
    }
}