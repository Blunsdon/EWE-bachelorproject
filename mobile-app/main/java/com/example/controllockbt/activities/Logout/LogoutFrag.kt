//package com.example.restapift.activities.Logout
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
//import com.example.controllockbt.repository.Repository
//
//
//class LogoutFrag : Fragment() {
//
//    private lateinit var viewModel: LogoutFragViewModel
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        // Inflate the layout for this fragment
//        val view = inflater.inflate(R.layout.fragment_logout_frag, container, false)
//
//
//        //Listener for next fragment button
//        view.findViewById<Button>(R.id.buttonLogoutNextPage).setOnClickListener{
//            //navigate to next fragment
//            Navigation.findNavController(view).navigate(R.id.action_logout_frag_to_login_frag)
//        }
//
//
//        //text field to display data in fragment
//        val textView : TextView = view.findViewById(R.id.test_text_view)
//        //get fragment arguments (the data bundle)
//        val args = this.arguments
//        //get a specific data entry in the bundle
//        val inputData = args?.get("token")
//        //display bundle data
//        val tokenText = inputData.toString()
//        textView.text = tokenText
//
//        //Button and listener for making the restAPI call
//        val getButton : Button = view.findViewById(R.id.buttonLogoutCall)
//        getButton.setOnClickListener{
//            //retrofit repo
//            val repository = Repository()
//            //retrofit modelFac
//            val viewModelFactory = LogoutFragModelFactory(repository)
//            //model extension
//            viewModel = ViewModelProvider(this, viewModelFactory).get(LogoutFragViewModel::class.java)
//            //push POST to restAPI
//            val tokenPlace = "Token "
//            val tokenString = tokenPlace.plus(tokenText)
//            viewModel.pushPost(tokenString)
//            //read response
//            viewModel.myResponse.observe(viewLifecycleOwner, { response ->
//                if(response.isSuccessful) {
//                    //got a response
//                    Log.d("response", response.body()?.auth_token.toString())
//                    Log.d("Response", response.message().toString())
//                    Log.d("Response", response.code().toString())
//                    textView.text = "User logged out"
//                }
//                else{
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