package com.example.controllockbt

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.activity.addCallback
import androidx.activity.result.ActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.navigation.Navigation

import androidx.lifecycle.ViewModelProvider
import com.example.controllockbt.activities.FacInfo.FacInfoModelFactory
import com.example.controllockbt.activities.FacInfo.FacInfoViewModel
import com.example.controllockbt.activities.Logout.LogoutFragModelFactory
import com.example.controllockbt.activities.Logout.LogoutFragViewModel
import com.example.controllockbt.model.PostGetFacInfo
import com.example.controllockbt.repository.Repository
import java.lang.IllegalArgumentException


class ScanFrag : Fragment() {
    private var mBluetoothAdapter: BluetoothAdapter? = null
    private lateinit var viewModel: FacInfoViewModel
    private lateinit var viewModel2: LogoutFragViewModel
    private val aLName = ArrayList<String>()
    private var chosenDeviceName: String = ""
    private val aLMac = ArrayList<String>()
    private var chosenDeviceMac: String = ""
    private lateinit var useremail: String
    private lateinit var token: String
    private val facilityAccess = ArrayList<String>()
    // Toast message function
    private fun showToast(msg: String) {
        Toast.makeText( context, msg, Toast.LENGTH_SHORT).show()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_scan, container, false)

        requireActivity().onBackPressedDispatcher.addCallback(this) {
            Log.d("bpc", "pressed back")
            logout()
        }

        //Get arguments
        val args = this.arguments
        //get a specific data entry in the bundle
        val inputData = args?.get("UserEmail")
        val inputToken = args?.get("Token")
        //display bundle data
        useremail = inputData.toString()
        token = inputToken.toString()
        val viewtest = view.findViewById<TextView>(R.id.textView)
        viewtest.text = useremail

        // Get facililty access
        facilityAccess(useremail, inputToken.toString())

        val bluetoothManager = context?.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        mBluetoothAdapter = bluetoothManager.adapter

        // Run Bluetooth checks
        checkBT()

        // finds log out button
        val btnLogOut = view.findViewById<Button>(R.id.btnLogOut)
        btnLogOut.setOnClickListener {
            logout()
        }

        // button for making new scans
        val btnScan = view.findViewById<Button>(R.id.btnScan)
        btnScan.setOnClickListener {
            showToast("Scanning started")
            val loadingInfo = view?.findViewById<TextView>(R.id.loadingInfo)
            if(!mBluetoothAdapter!!.isDiscovering) {
                loadingInfo?.text = "Scanning error wait 10 seconds"
                }
            startBT()
            }

        return view
    }

    private fun logout(){
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = LogoutFragModelFactory(repository)
        //model extension
        viewModel2 = ViewModelProvider(this, viewModelFactory).get(LogoutFragViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(token)
        viewModel2.pushPost(tokenString)
        //read response
        viewModel2.myResponse.observe(viewLifecycleOwner, { response ->
            if(response.isSuccessful) {
                // Go back to login fragment
                Log.d("Response", response.code().toString())
                showToast("Logged out")
                view?.let { Navigation.findNavController(it).navigate(R.id.action_scanFrag_to_loginFrag) }
            }
            else{
                //no response
                Log.d("Response-error", response.message().toString())
                Log.d("Response-error", response.code().toString())
            }
        })
    }


    private fun startBT() {
        Log.d("sf_startBt", "function started")
        val permissionCheck = ContextCompat.checkSelfPermission(
            requireActivity(),
            Manifest.permission.ACCESS_FINE_LOCATION
        )
        if (permissionCheck == PackageManager.PERMISSION_GRANTED){
            Log.d("sf_startBt", "permissions granted")
            // Register for broadcasts when a device is discovered.
            val filter = IntentFilter().apply {
                addAction(BluetoothDevice.ACTION_FOUND)
                addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED)
                addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
            }

            if (mBluetoothAdapter?.isDiscovering!!) {
                mBluetoothAdapter!!.cancelDiscovery()
                Log.d("test", "Canceling discovery.")
                mBluetoothAdapter!!.startDiscovery()
                // Register receiver
                requireActivity().registerReceiver(receiver, filter)
            }else{
                Log.d("test", "Starting discovery.")
                mBluetoothAdapter!!.startDiscovery()
                // Register receiver
                requireActivity().registerReceiver(receiver, filter)
            }
        }
        else{
            Log.d("sf_startBt", "permissions not granted")
            showToast("Bluetooth must be enabled")
        }
    }

    // Get facility access info
    @SuppressLint("SetTextI18n")
    private fun facilityAccess(useremail: String, token: String){
        //retrofit repo
        val repository = Repository()
        //retrofit modelFac
        Log.d("tester", useremail)
        Log.d("tester", token)
        val viewModelFactory = FacInfoModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(FacInfoViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(token)
        val myPost = PostGetFacInfo(useremail, emptyList())
        viewModel.pushPost(tokenString, myPost)
        //read response
        viewModel.myResponse.observe(viewLifecycleOwner, { response ->
            Log.d("Iam IN", response.code().toString())
            if (response.isSuccessful) {
                val progressBar: ProgressBar? = view?.findViewById(R.id.scanningBar)
                val loadingInfo = view?.findViewById<TextView>(R.id.loadingInfo)
                val listOfScanning = view?.findViewById<ListView>(R.id.scanResult)
                val buttonScan = view?.findViewById<Button>(R.id.btnScan)
                if(response.body()?.list.isNullOrEmpty()){
                    Log.d("Response msg", "NO facility access")
                    // Remove all features
                    loadingInfo?.text = "You have NO access to any facility"
                    // Make Visible
                    progressBar?.visibility = View.INVISIBLE
                    // Make Invisible
                    listOfScanning?.visibility = View.INVISIBLE
                    buttonScan?.visibility = View.INVISIBLE
                }else{

                    // Remove all features
                    loadingInfo?.text = "Press Scan to scan for facilities"
                    // Make Invisible
                    progressBar?.visibility = View.INVISIBLE
                    listOfScanning?.visibility = View.INVISIBLE
                    // Make Visible
                    buttonScan?.visibility = View.VISIBLE
                    Log.d("Response msg", response.message().toString())
                    Log.d("Response code", response.code().toString())
                    // get all facilities
                    for(item in response.body()?.list!!){
                        Log.d("Response string", item[0])
                        facilityAccess.add(item[0])
                    }

                }
            } else {
                //no response
                Log.d("Response-error", response.message().toString())
                Log.d("Response-error", response.code().toString())
            }
        })
    }


    private fun checkBT(){
        if (mBluetoothAdapter == null) {
            showToast("This device doesn't support Bluetooth")
        }

        // start BT if user has access to facilities
        //make sure bluetooth is enabled.
        if(!mBluetoothAdapter!!.isEnabled){
            showToast("Bluetooth is OFF, trying to turn ON")
            val enableBluetoothIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            resultContract.launch(enableBluetoothIntent)
            showToast("Bluetooth is turned ON!")
        }else{
            if(mBluetoothAdapter!!.isEnabled){
            }
        }
    }

    // Checking Bluetooth
    private val resultContract = registerForActivityResult(ActivityResultContracts.StartActivityForResult())
    { result: ActivityResult? ->
        if(result?.resultCode == Activity.RESULT_OK) {
            showToast("Bluetooth has been enabled")
        } else {
            showToast("Bluetooth has been disabled")
        }
    }

    // receiver for Bluetooth
    private val receiver = object : BroadcastReceiver() {
        @SuppressLint("CutPasteId", "SetTextI18n") //TODO: fix
        override fun onReceive(context: Context, intent: Intent) {
            val progressBar: ProgressBar? = view?.findViewById(R.id.scanningBar)
            val loadingInfo = view?.findViewById<TextView>(R.id.loadingInfo)
            val listOfScanning = view?.findViewById<ListView>(R.id.scanResult)
            val buttonScan = view?.findViewById<Button>(R.id.btnScan)
            when(intent.action) {
                BluetoothDevice.ACTION_FOUND -> {
                    // Discovery has found a device. Get the BluetoothDevice
                    // object and its info from the Intent.
                    val device: BluetoothDevice? = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
                    val deviceName = device?.name.toString()
                    Log.d("deviceName", "" + deviceName)
                    val deviceHardwareAddress = device?.address.toString() // MAC address
                    Log.d("deviceHardwareAddress", "" + deviceHardwareAddress)
                    // filter founded devices
                    if(deviceName.contains("facility")){
                        // Get MAC address
                        val deviceHardwareAddress = device?.address.toString()
                        Log.d("deviceHardwareAddress", "" + deviceHardwareAddress)
                        // Add  to list
                        aLMac.add(deviceHardwareAddress)
                        aLName.add(deviceName)
                    } else {
                        Log.d("action found", "discarded null named device")
                    }
                }
                BluetoothAdapter.ACTION_DISCOVERY_STARTED ->{
                    // Make sure lists are cleared
                    aLMac.clear()
                    aLName.clear()
                    loadingInfo?.text = "Scanning for facilities"
                    // Make Visible
                    progressBar?.visibility = View.VISIBLE
                    // Make Invisible
                    listOfScanning?.visibility = View.INVISIBLE
                    buttonScan?.visibility = View.INVISIBLE
                }
                BluetoothAdapter.ACTION_DISCOVERY_FINISHED -> {
                    Log.d("test", "in discovery finished receiver")
                    loadingInfo?.text = "Scanning complete"
                    // Make Invisible
                    progressBar?.visibility = View.INVISIBLE
                    // Make Visible
                    listOfScanning?.visibility = View.VISIBLE
                    buttonScan?.visibility = View.VISIBLE

                    if(aLMac.isEmpty()){
                        // No facilities founded
                        Log.d("LIST EMPTY: ", "EMPTY MAC list")
                        // listView setup with NO facilities founded
                        val noneFound = ArrayList<String>()
                        noneFound.add("No facilities found, try to scan again")
                        val adapter = context.let { ArrayAdapter(it, R.layout.custom_list_item, noneFound)}
                        val selectDeviceList: ListView? = view?.findViewById(R.id.scanResult)
                        selectDeviceList?.adapter = adapter
                        Log.d("Bundle: ", "username: " + useremail)
                        Log.d("Bundle: ", "token: " + token)
                    }else{
                        val showList = ArrayList<String>()
                        val MacList = ArrayList<String>()
                        // compare all facilities with founded devices
                        for(item in facilityAccess){
                            var index = 0
                            for(name in aLName){
                                if(item == name){
                                    showList.add(name)
                                    MacList.add(aLMac[index])
                                }
                                index += 1
                            }
                        }
                        // listView setup
                        val adapter = context.let { ArrayAdapter(it, R.layout.custom_list_item, showList)}
                        val selectDeviceList: ListView? = view?.findViewById(R.id.scanResult)
                        selectDeviceList?.adapter = adapter
                        selectDeviceList?.setOnItemClickListener{_,_,position,_ ->
                            chosenDeviceName = showList[position]
                            Log.d("arguments ff: ", "CDN: " + chosenDeviceName)
                            chosenDeviceMac = MacList[position]
                            Log.d("arguments ff: ", "CDM: " + chosenDeviceMac)
                            // make bundle
                            val bundle = Bundle()
                            bundle.putString("UserEmail", useremail)
                            Log.d("Bundle: ", "username: $useremail")
                            bundle.putString("Token", token)
                            Log.d("Bundle: ", "token: $token")
                            bundle.putString("MacAdress", chosenDeviceMac)
                            bundle.putString("FacName", chosenDeviceName)
                            view?.let { Navigation.findNavController(it).navigate(R.id.action_scanFrag_to_unlockFrag, bundle) }
                        }
                    }
                }
            }
        }
    }

    override fun onDestroy() {
        try {
            if (receiver != null) {
                activity?.unregisterReceiver(receiver)
            }
        } catch (e: IllegalArgumentException) {
            e.printStackTrace()
        }
        super.onDestroy()
    }
}

