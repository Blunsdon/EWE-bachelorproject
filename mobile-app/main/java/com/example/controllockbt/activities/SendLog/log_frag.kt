//package com.example.restapift.activities.SendLog
//
//import android.media.FaceDetector
//import android.os.Bundle
//import android.util.Log
//import androidx.fragment.app.Fragment
//import android.view.LayoutInflater
//import android.view.View
//import android.view.ViewGroup
//import android.widget.Button
//import android.widget.TextView
//import androidx.lifecycle.ViewModelProvider
//import androidx.navigation.Navigation
//import com.example.restapift.R
//import com.example.controllockbt.activities.FacInfo.FacInfoModelFactory
//import com.example.controllockbt.activities.FacInfo.FacInfoViewModel
//import com.example.controllockbt.model.Facility
//import com.example.controllockbt.model.PostGetFacInfo
//import com.example.controllockbt.model.PostSendLog
//import com.example.controllockbt.repository.Repository
//
//
//class log_frag : Fragment() {
//
//    private lateinit var viewModel: SendLogViewModel
//    private var tokenString = "none"
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        // Inflate the layout for this fragment
//        val view = inflater.inflate(R.layout.fragment_log_frag, container, false)
//
//        //Get arguments
//        val args = this.arguments
//        //get a specific data entry in the bundle
//        val inputData = args?.get("token")
//        //display bundle data
//        tokenString = inputData.toString()
//
//        //Listener for next fragment button
//        view.findViewById<Button>(R.id.buttonLogNextPage).setOnClickListener{
//            //create bundle
//            val bundle = Bundle()
//            //insert bundle data
//            bundle.putString("token", tokenString)
//            //navigate to next fragment
//            Navigation.findNavController(view).navigate(R.id.action_log_frag_to_logout_frag, bundle)
//        }
//
//        val textView : TextView = view.findViewById(R.id.TextViewLog)
//        textView.text = "No key retrieved yet!"
//
//        //Button and listener for making the restAPI call
//        val getButton : Button = view.findViewById(R.id.buttonSendLog)
//        getButton.setOnClickListener{
//            //retrofit repo
//            val repository = Repository()
//            //retrofit modelFac
//            val viewModelFactory = SendLogModelFactory(repository)
//            //model extension
//            viewModel = ViewModelProvider(this, viewModelFactory).get(SendLogViewModel::class.java)
//            //push POST to restAPI
//            val tokenPlace = "Token "
//            val tokenString = tokenPlace.plus(tokenString)
//
//            var fac: List<Facility> = listOf(Facility("test facility 1"))
//            var log: List<com.example.controllockbt.model.Log> = listOf(com.example.controllockbt.model.Log("field", "ewe", "2021-10-10T23:44:22", "field@field.com", "test facility 1", "herning"))
//
//
//            val myPost = PostSendLog(fac, log,"")
//
//            viewModel.pushPost(tokenString, myPost)
//            //read response
//            viewModel.myResponse.observe(viewLifecycleOwner, { response ->
//                if (response.isSuccessful) {
//                    //got a response
//                    Log.d("Response msg", response.message().toString())
//                    Log.d("Response code", response.code().toString())
//                    textView.text = response.body()?.key
//                } else {
//                    //no response
//                    Log.d("Response-error", response.message().toString())
//                    Log.d("Response-error", response.code().toString())
//                }
//            })
//        }
//        return view
//    }
//}