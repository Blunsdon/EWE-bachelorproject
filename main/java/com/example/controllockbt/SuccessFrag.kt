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
import androidx.navigation.Navigation


class SuccessFrag : Fragment() {

    // Bundle variables
    private var tokenString: String = ""
    private var userEmailString = ""
    private var facNameString = ""

    // For counter
    lateinit var counter: TextView


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        var view = inflater.inflate(R.layout.fragment_success, container, false)
        val timer = MyCounter(5000, 1000)
        timer.start()

        counter = view.findViewById(R.id.textViewSuccess)

        // get arguments
        val args = this.arguments
        var token = args?.get("Token")
        var userEmail = args?.get("UserEmail")
        var facName = args?.get("FacName")
        //Assign arguments (production)
        tokenString = token.toString()
        userEmailString = userEmail.toString()
        facNameString = facName.toString()

        var button: Button = view.findViewById(R.id.buttonBackSuccess)
        button.visibility = View.VISIBLE
        button.setOnClickListener{
            var bundle = Bundle()
            bundle.putString("Token", tokenString)
            bundle.putString("UserEmail", userEmailString)
            bundle.putString("FacName", facNameString)
            Navigation.findNavController(view).navigate(R.id.action_successFrag_to_scanFrag, bundle)
        }

        return view
    }

    inner class MyCounter(millisInFuture: Long, countDownInterval: Long): CountDownTimer(millisInFuture, countDownInterval){
        override fun onFinish() {
            Log.d("countDown", "CountDown done!")
            counter.text = ("Door is locked!")
        }

        override fun onTick(millisUntilFinished: Long) {
            var ms = millisUntilFinished + 1000
            counter.text = ("Door is unlocked " + ms/1000).toString() + " seconds"
        }
    }

}