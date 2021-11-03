package com.example.controllockbt

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.Navigation
import com.example.controllockbt.activities.Login.LoginFragModelFactory
import com.example.controllockbt.activities.Login.LoginFragViewModel
import com.example.controllockbt.model.PostLogin
import com.example.controllockbt.repository.Repository


class LoginFrag : Fragment() {
        private lateinit var viewModel: LoginFragViewModel

    //  Function for opening web page
    fun openWebPage(url: String) {
        val webpage: Uri = Uri.parse(url)
        val intent = Intent(Intent.ACTION_VIEW, webpage)
        startActivity(intent)
    }

    // Toast message function
    private fun showToast(msg: String) {
        Toast.makeText( context, msg, Toast.LENGTH_SHORT).show()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_login, container, false)

        // Find button for create user
        val btnCreateUser = view.findViewById<Button>(R.id.btnCreateUser);
        // Create new user
        btnCreateUser.setOnClickListener {
            showToast("Redirect to Create User URL")
            // Redirect to Create new user page in browser
            openWebPage("http://www.control-center.xyz/create_user/")
        }

        // Find button for login
        val btnLogin = view.findViewById<Button>(R.id.btnLogin);
        // Login
        btnLogin.setOnClickListener {
            // Get inputs
            val viewEmail = view.findViewById<EditText>(R.id.editTextTextEmailAddress)
            val viewPassword = view.findViewById<EditText>(R.id.editTextTextPassword)
            // Login message
            showToast("Login Clicked")
            //retrofit repo
            val repository = Repository()
            //retrofit modelFac
            val viewModelFactory = LoginFragModelFactory(repository)
            //model extension
            viewModel = ViewModelProvider(this, viewModelFactory).get(LoginFragViewModel::class.java)
            val myPost = PostLogin(viewEmail.text.toString(), viewPassword.text.toString(), auth_token = "")
            //push POST to restAPI
            viewModel.pushPost(myPost)
            // Error message view
            val errormsg = view.findViewById<TextView>(R.id.errorText)
            // Check response
            viewModel.myResponse.observe(viewLifecycleOwner, { response ->
                // check if login successful
                if(response.code() == 200) {
                    // Create bundle
                    val bundle = Bundle()
                    bundle.putString("useremail", viewEmail.text.toString())
                    bundle.putString("token", response.body()?.auth_token.toString())
                    // Redirect to ScanFrag
                    Navigation.findNavController(view).navigate(R.id.scanFrag, bundle)
                }
                else{
                    // Failed to login send error message
                    errormsg.visibility = View.VISIBLE
                }
            })
        }
        return view
    }
}