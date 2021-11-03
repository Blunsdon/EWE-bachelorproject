import android.util.Log

//package com.example.restapift.activities.FacInfo
//
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
//import com.example.controllockbt.model.PostGetFacInfo
//import com.example.controllockbt.repository.Repository
//
//
//class FacInfo_frag : Fragment() {
//
//    private lateinit var viewModel: FacInfoViewModel
//    private var tokenString = "none"
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        // Inflate the layout for this fragment
//        val view = inflater.inflate(R.layout.fragment_fac_info_frag, container, false)
//
//        //Get arguments
//        val args = this.arguments
//        //get a specific data entry in the bundle
//        val inputData = args?.get("token")
//        //display bundle data
//        tokenString = inputData.toString()
//
//        //Listener for next fragment button
//        view.findViewById<Button>(R.id.buttonFacInfoNextPage).setOnClickListener{
//            //create bundle
//            val bundle = Bundle()
//            //insert bundle data
//            bundle.putString("token", tokenString)
//            //navigate to next fragment
//            Navigation.findNavController(view).navigate(R.id.action_facInfo_frag_to_log_frag, bundle)
//        }
//
//        val textView : TextView = view.findViewById(R.id.textViewFacInfo)
//        textView.text = "No info collected yet!"
//
//        //Button and listener for making the restAPI call
//        val getButton : Button = view.findViewById(R.id.buttonFacilityInfo)
//        getButton.setOnClickListener{
//            //retrofit repo
//            val repository = Repository()
//            //retrofit modelFac
//            val viewModelFactory = FacInfoModelFactory(repository)
//            //model extension
//            viewModel = ViewModelProvider(this, viewModelFactory).get(FacInfoViewModel::class.java)
//            //push POST to restAPI
//            val tokenPlace = "Token "
//            val tokenString = tokenPlace.plus(tokenString)
//            val myPost = PostGetFacInfo("field@field.com", emptyList())
//            viewModel.pushPost(tokenString, myPost)
//            //read response
//            viewModel.myResponse.observe(viewLifecycleOwner, { response ->
//                if (response.isSuccessful) {
//                    //got a response
//                        if(response.body()?.list.isNullOrEmpty()){
//                            Log.d("Response msg", "NO facility access")
//                        }else{
//                            Log.d("Response msg", response.message().toString())
//                            Log.d("Response code", response.code().toString())
//                            Log.d("Response string", response.body()?.list?.get(0).toString())
//                            //textView.text = response.body()?.list.toString()
//                        }
//                } else {
//                    //no response
//                    Log.d("Response-error", response.message().toString())
//                    Log.d("Response-error", response.code().toString())
//                }
//            })
//        }
//
//        return view
//    }
//
//}