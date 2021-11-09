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
import android.widget.Toast
import androidx.activity.addCallback
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
import okio.ByteString.Companion.readByteString
import java.io.BufferedReader
import java.io.IOException
import java.time.Instant
import java.time.format.DateTimeFormatter
import java.util.*
import java.util.logging.Logger.global

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

    //toast
    private fun showToast(msg: String) {
        Toast.makeText( context, msg, Toast.LENGTH_SHORT).show()
    }


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

        //response okay -> launch coroutines
        var job = CoroutineScope(Dispatchers.IO).launch {
            connectBt()
        }

        // This callback will only be called when MyFragment is at least Started.
        requireActivity().onBackPressedDispatcher.addCallback(this) {
            Log.d("bpc", "pressed back")
            showToast("Back not allowed while unlocking")
        }

        return view
    }

    private fun sendLog(){
        var logReturn: Boolean
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = SendLogModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(SendLogViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(Token)

        var fac: List<Facility> = listOf(Facility(FacName))
        var log: List<com.example.controllockbt.model.Log> = listOf(com.example.controllockbt.model.Log(DateTimeFormatter.ISO_INSTANT.format(
            Instant.now()), UserEmail, FacName))
        val myPost = PostSendLog(fac, log,"")

        viewModel.pushPost(tokenString, myPost)
        //read response
        viewModel.myResponse.observe(viewLifecycleOwner, { response ->
            if (response.isSuccessful) {
                //got a response
                keyString = response.body()?.key.toString()

                logSucces = true
            } else {
                //no response
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
            var bundle = Bundle()
            bundle.putString("Token", Token)
            bundle.putString("UserEmail", UserEmail)
            bundle.putString("FacName", FacName)
            bundle.putString("StatusCode", code)
            view?.let { Navigation.findNavController(it).navigate(R.id.action_unlockFrag_to_successFrag, bundle)}
        } else {
            progressBar?.visibility = View.VISIBLE
            textCode?.text = "Unlocking door!"
        }
    }

    private fun sendCommand(input: String, view: View): String {
        Log.d("SCCode", keyString)
        if(mBluetoothSocket != null){
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
                                    cleanSocket()
                                    return "200"
                                }
                                if (readMsg.contains("500")) {
                                    cleanSocket()
                                    return("500")
                                }
                                if (readMsg.contains("401")) {
                                    cleanSocket()
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
                Log.e("sendCommand error", e.toString())
            }
        }
        return "200"
    }

    private fun cleanSocket(){
        Log.d("CloseSocket_sc", "closing socket connections")
        if(mBluetoothSocket!!.isConnected == true) {
            try {
                Log.d("CloseSocket_sc", "closing s.input: " + mBluetoothSocket?.inputStream?.available())
                mBluetoothSocket?.inputStream?.close()
            } catch (e: IOException) {
                Log.d("CloseSocket_sc", "Could not close the client socket inputstream", e)
            }
            try {
                Log.d("CloseSocket_sc", "closing s.output")
                mBluetoothSocket?.outputStream?.close()
            } catch (e: IOException) {
                Log.d("CloseSocket_sc", "Could not close the client socket outputstream", e)
            }
            try {
                Log.d("CloseSocket_sc", "closing socket")
                mBluetoothSocket?.close()
            } catch (e: IOException) {
                Log.d("CloseSocket_sc", "Could not close the client socket", e)
            }
            mBluetoothSocket = null
            mIsConnected = false
        } else {
            Log.d("CloseSocket_sc", "socket not connected")
        }
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
                } catch (e: IOException){
                    navigate("500")
                }
                mIsConnected = true
                var SCstring: String? = view?.let { sendCommand("42", it) }
                if (SCstring != null) {
                    editMainThread("done", SCstring)
                } else {
                    editMainThread("done", "500")
                }

            } else {
                editMainThread("done", "500")
            }
        } catch (e: IOException) {
            editMainThread("done", "500")
            mIsConnected = false
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
}