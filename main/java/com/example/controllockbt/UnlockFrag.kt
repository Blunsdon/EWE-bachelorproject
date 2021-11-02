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
import android.widget.TextView
import androidx.lifecycle.ViewModelProvider
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

// TODO: change restapi, so all fields are included for log etc. company name

class UnlockFrag : Fragment() {
    // Test variables
    private var test_tokenString: String = "b94e2e24552912d0677f637d2b34f1b310f904f7"
    private var test_userEmailString = "field@field.com"
    private var test_facNameString = "facility pi"
    private var test_macString: String = "B8:27:EB:6C:B3:E0"
    private var test_companyString: String = "mob test"
    private var test_facLocation: String = "test location"

    // Bundle variables
    private var tokenString: String = ""
    private var userEmailString = ""
    private var facNameString = ""
    private var macString: String = ""
    private var keyString: String = ""

    // Bluetooth variables
    private var mMyUUID: UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
    private var mBluetoothSocket: BluetoothSocket? = null
    private lateinit var mBluetoothAdapter: BluetoothAdapter
    private var mIsConnected: Boolean = false

    // restAPI variables
    private lateinit var viewModel: SendLogViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_unlock, container, false)

//        // get arguments
//        val args = this.arguments
//        var token = args?.get("Token")
//        var userEmail = args?.get("UserEmail")
//        var facName = args?.get("FacName")
//        var macAddress = args?.get("MacAdress")
//        //Assign arguments (production)
//        tokenString = token.toString()
//        userEmailString = userEmail.toString()
//        facNameString = facName.toString()
//        macString = macAddress.toString()
        //Assign arguments (test)
        tokenString = test_tokenString
        userEmailString = test_userEmailString
        facNameString = test_facNameString
        macString = test_macString

        sendLog()

        CoroutineScope(Dispatchers.IO).launch {
            connectBt(view)
        }

        return view
    }

    private suspend fun editMainThread(status: String) {
        withContext(Dispatchers.Main) {
            setNewStatus(status)
            if(mIsConnected){
                view?.let { sendCommand(keyString, it) }
            }
        }
    }

    private fun setNewStatus(status: String){
        val textUnlock: TextView? = view?.findViewById(R.id.textViewUnlock)
        if(status != "done"){
            textUnlock?.text = "Unlocking door!"
        }
    }

    private fun sendCommand(input: String, view: View) {
        Log.d("Code", input)
        if(mBluetoothSocket != null){
            try {
                mBluetoothSocket!!.outputStream.write(input.toByteArray())
            } catch (e: IOException) {
                e.printStackTrace()
            }
            try {
                mBluetoothSocket!!.close()
                mBluetoothSocket = null
                mIsConnected = false
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }

        Log.d("unlock debug", "creating bundle")
        var bundle = Bundle()
        bundle.putString("Token", tokenString)
        bundle.putString("UserEmail", userEmailString)
        bundle.putString("FacName", facNameString)
        Log.d("unlock debug", "sending bundle + nav shift")
        val navcontroller = this.findNavController()
        navcontroller.navigate(R.id.action_unlockFrag_to_successFrag, bundle)
    }

    private fun sendLog(){
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = SendLogModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(SendLogViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(tokenString)

        // TODO: change to correct variables after restAPI is fixed
        var fac: List<Facility> = listOf(Facility(facNameString))
        var log: List<com.example.controllockbt.model.Log> = listOf(com.example.controllockbt.model.Log(userEmailString, test_companyString, DateTimeFormatter.ISO_INSTANT.format(
            Instant.now()), userEmailString, facNameString, test_facLocation))


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
            } else {
                //no response
                Log.d("restAPI: Response-error", response.message().toString())
                Log.d("restAPI: Response-error", response.code().toString())
            }
        })
    }

    private suspend fun connectBt(view: View) {
        editMainThread("start")
        try {
            if(mBluetoothSocket == null || !mIsConnected) {
                val bluetoothManager = context?.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
                mBluetoothAdapter = bluetoothManager.adapter
                val device: BluetoothDevice = mBluetoothAdapter.getRemoteDevice(macString)
                kotlin.runCatching {mBluetoothSocket = device.createInsecureRfcommSocketToServiceRecord(mMyUUID)}
                bluetoothManager.adapter.cancelDiscovery()
                kotlin.runCatching {mBluetoothSocket!!.connect()}
                mIsConnected = true
            }
        }catch (e: IOException) {
            mIsConnected = false
            e.printStackTrace()
        }
        editMainThread("done")
    }
    
}