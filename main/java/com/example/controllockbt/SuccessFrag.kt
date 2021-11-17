package com.example.controllockbt

import android.content.IntentSender
import android.os.Bundle
import android.os.CountDownTimer
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.addCallback
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.Navigation
import com.example.controllockbt.activities.Logout.LogoutFragModelFactory
import com.example.controllockbt.activities.Logout.LogoutFragViewModel
import com.example.controllockbt.repository.Repository


class SuccessFrag : Fragment() {

    // Logout var
    private lateinit var viewModel: LogoutFragViewModel

    // Bundle variables
    private var tokenString: String = ""
    private var userEmailString = ""
    private var facNameString = ""
    private var statusString: String = ""
    private var vis: Boolean = false

    // For counter
    lateinit var counter: TextView

    //toast
    //toast
    private fun showToast(msg: String) {
        Toast.makeText( context, msg, Toast.LENGTH_SHORT).show()
    }


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        var view = inflater.inflate(R.layout.fragment_success, container, false)

        // This callback will only be called when MyFragment is at least Started.
        requireActivity().onBackPressedDispatcher.addCallback(this) {
            Log.d("bpc", "pressed back")
            showToast("Not allowed!")
        }

        val timer = MyCounter(5000, 1000)
        timer.start()

        counter = view.findViewById(R.id.textViewSuccess)

        // get arguments
        val args = this.arguments
        var token = args?.get("Token")
        var userEmail = args?.get("UserEmail")
        var facName = args?.get("FacName")
        var status = args?.get("StatusCode")
        //Assign arguments (production)
        tokenString = token.toString()
        userEmailString = userEmail.toString()
        facNameString = facName.toString()
        statusString = status.toString()

        var button: Button = view.findViewById(R.id.buttonBackSuccess)
        button.visibility = View.INVISIBLE //invisible

        button.setOnClickListener {
            var bundle = Bundle()
            bundle.putString("Token", tokenString)
            bundle.putString("UserEmail", userEmailString)
            bundle.putString("FacName", facNameString)
            if(status == "200") {
                Navigation.findNavController(view)
                    .navigate(R.id.action_successFrag_to_scanFrag, bundle)
            }
            if(status == "500") {
                Navigation.findNavController(view)
                    .navigate(R.id.action_successFrag_to_scanFrag, bundle)
            }
            if(status == "401") {
                logout()
                Navigation.findNavController(view)
                    .navigate(R.id.action_successFrag_to_loginFrag)
            }
        }

        return view
    }

    private fun logout(){
        //retrofit repo
        val repository = Repository()
        //retrofit modelFac
        val viewModelFactory = LogoutFragModelFactory(repository)
        //model extension
        viewModel = ViewModelProvider(this, viewModelFactory).get(LogoutFragViewModel::class.java)
        //push POST to restAPI
        val tokenPlace = "Token "
        val tokenString = tokenPlace.plus(tokenString)
        viewModel.pushPost(tokenString)
    }

    inner class MyCounter(millisInFuture: Long, countDownInterval: Long): CountDownTimer(millisInFuture, countDownInterval){
        override fun onFinish() {
            Log.d("countDown", "CountDown done!")
            var button: Button? = view?.findViewById(R.id.buttonBackSuccess)
            button?.visibility = View.VISIBLE
            if(statusString == "200") {
                button?.text = "Go to scan"
                counter.text = ("Return to scanning")
            }
            if(statusString == "500") {
                button?.text = "Go to scan"
                counter.text = ("Return to scanning")
            }
            if(statusString == "401") {
                button?.text = "Logout"
                counter.text = ("Return to login")
            }

        }

        override fun onTick(millisUntilFinished: Long) {
            var ms = millisUntilFinished + 1000
            if(statusString == "200") {
                counter.text = ("Door is unlocked for " + (ms/1000).toString() + " sec.")
            }
            if(statusString == "500") {
                counter.text = ("Internal Error happened (" + (ms/1000).toString() + ")")
            }
            if(statusString == "401") {
                counter.text = ("Not authorized for this facility (" + (ms/1000).toString() + ")")
            }
        }
    }

}