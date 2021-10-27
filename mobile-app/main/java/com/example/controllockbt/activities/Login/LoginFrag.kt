//package com.example.restapift.activities.Login
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
//import com.example.controllockbt.model.PostLogin
//import com.example.controllockbt.repository.Repository
//
//
//class LoginFrag : Fragment() {
//
//    private lateinit var viewModel: LoginFragViewModel
//    private var tokenString = "none"
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        // Inflate the layout for this fragment
//        val view = inflater.inflate(R.layout.fragment_login_frag, container, false)
//
//        //Listener for next fragment button
//        view.findViewById<Button>(R.id.buttonLoginNextPage).setOnClickListener{
//            //create bundle
//            val bundle = Bundle()
//            //insert bundle data
//            bundle.putString("token", tokenString)
//            //navigate to next fragment
//            Navigation.findNavController(view).navigate(R.id.action_login_frag_to_facInfo_frag, bundle)
//        }
//
//        //Button and listener for making the restAPI call
//        val getButton : Button = view.findViewById(R.id.buttonToken)
//        getButton.setOnClickListener{
//            //fragment text box
//            val tokenText : TextView = view.findViewById(R.id.textViewToken)
//            //retrofit repo
//            val repository = Repository()
//            //retrofit modelFac
//            val viewModelFactory = LoginFragModelFactory(repository)
//            //model extension
//            viewModel = ViewModelProvider(this, viewModelFactory).get(LoginFragViewModel::class.java)
//            //the restAPI POST data
//            val myPost = PostLogin("field@field.com", "field", auth_token = "")
//            //push POST to restAPI
//            viewModel.pushPost(myPost)
//            //read response
//            viewModel.myResponse.observe(viewLifecycleOwner, { response ->
//                if(response.isSuccessful) {
//                    //got a response
//                    Log.d("response", response.body()?.email.toString())
//                    Log.d("response", response.body()?.password.toString())
//                    Log.d("response", response.body()?.auth_token.toString())
//                    tokenString = response.body()?.auth_token.toString()
//                    tokenText.text = tokenString
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