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
import java.io.BufferedReader
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

    private val mmBuffer: ByteArray = ByteArray(3)
    private var logSucces: Boolean = false

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

        //response okay -> launch coroutines
        CoroutineScope(Dispatchers.IO).launch {
            connectBt()
        }

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

                logSucces = true

            } else {
                //no response
                Log.d("restAPI: Response-error", response.message().toString())
                Log.d("restAPI: Response-error", response.code().toString())

                // TODO: bad response do something!
            }
        })
    }

    private suspend fun editMainThread(status: String, code: String) {
        withContext(Dispatchers.Main) {
            setNewStatus(status, code)
        }
    }

    private fun setNewStatus(status: String, code: String){
        val progressBar: ProgressBar? = view?.findViewById(R.id.progressBarUnlock)
        val textCode: TextView? = view?.findViewById(R.id.textViewUnlock)
        if(status == "done"){
            navigate(code)
        } else {
            progressBar?.visibility = View.VISIBLE
            textCode?.text = "Unlocking door!"
        }
    }

    private fun sendCommand(input: String, view: View): String {
        Log.d("SCCode", keyString)
        if(mBluetoothSocket != null){
            Log.d("sendCommand", "Socket not null")
            Log.d("input_stream_before", mBluetoothSocket!!.inputStream.available().toString())
            try {
                if(mBluetoothSocket!!.isConnected == true) {
                    var loopControl: Boolean = false
                    var msgControl: Boolean = false
                    var loopCount: String = "0"
                    while(!loopControl){
                        if(logSucces) {
                            if(!msgControl) {
                                Log.d("sendCommand", "Sending msg: " + keyString)
                                mBluetoothSocket!!.outputStream.write(keyString.toByteArray())
                                msgControl = true
                            }

                            if(mBluetoothSocket!!.inputStream.available().toString() != "0") {
                                Log.d("input_stream_after", mBluetoothSocket!!.inputStream.available().toString())
                                mBluetoothSocket!!.inputStream.read(mmBuffer)
                                var readMsg = String(mmBuffer)
                                Log.d("input_stream", readMsg)
                                if (readMsg.contains("200")) {
                                    loopControl = true
                                }
                                if (readMsg.contains("500")) {
                                    return("500")
                                }
                                if (readMsg.contains("401")) {
                                    return("401")
                                }
                            }

                            loopCount += "1"
                            if(loopCount == "5") {
                                loopCount = "0"
                                msgControl = false
                            }
                        }
                    }
                }

            } catch (e: IOException) {
                Log.d("sendCommand error", e.toString())
            }
            try {
                if(mBluetoothSocket!!.isConnected == true) {
                    try {
                        Log.d("CloseSocket_sc", "Closing inputstream")
                        mBluetoothSocket?.inputStream?.close()
                    } catch (e: IOException) {
                        Log.d("CloseSocket_sc", "Could not close the client socket inputstream", e)
                    }
                    try {
                        Log.d("CloseSocket_sc", "Closing outputstream")
                        mBluetoothSocket?.outputStream?.close()
                    } catch (e: IOException) {
                        Log.d("CloseSocket_sc", "Could not close the client socket outputstream", e)
                    }
                    try {
                        Log.d("CloseSocket_sc", "Closing socket")
                        mBluetoothSocket?.close()
                    } catch (e: IOException) {
                        Log.d("CloseSocket_sc", "Could not close the client socket", e)
                    }
                    mBluetoothSocket = null
                    mIsConnected = false
                }
            } catch (e: IOException) {
                e.printStackTrace()
            }
            Log.d("CloseSocket_SC_isConnected", mBluetoothSocket?.isConnected.toString())
        }
        return "200"
    }

    private suspend fun connectBt() {
        editMainThread("start", "0")
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
                    navigate("500")
                }
                mIsConnected = true
                Log.d("connectBt", "success: BtSocket created")
                var SCstring: String? = view?.let { sendCommand("42", it) }
                if (SCstring != null) {
                    editMainThread("done", SCstring)
                } else {
                    editMainThread("done", "500")
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

    private fun navigate(status: String){
        var bundle = Bundle()
        bundle.putString("Token", Token)
        bundle.putString("UserEmail", UserEmail)
        bundle.putString("FacName", FacName)
        bundle.putString("StatusCode", status)
        view?.let { Navigation.findNavController(it).navigate(R.id.action_unlockFrag_to_successFrag, bundle) }
    }

    override fun onDestroy() {
        try {
            Log.d("CloseSocket_od_isConnected", mBluetoothSocket?.isConnected.toString())

        } catch (e: IOException) {
            Log.e("CloseSocket_od", "Could not close the client socket", e)
        }
        super.onDestroy()
    }
}