package com.example.controllockbt

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView


class ScanFrag : Fragment() {


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_scan, container, false)


        //Get arguments
        val args = this.arguments
        //get a specific data entry in the bundle
        val inputData = args?.get("useremail")
        val inputData2 = args?.get("password")
        val token = args?.get("token")

        //display bundle data
        val tokenString = inputData.toString()
        val tokenString2 = inputData2.toString()
        val tokenString3 = token.toString()

        val viewtest = view.findViewById<TextView>(R.id.textView)
        val viewtest2 = view.findViewById<TextView>(R.id.textView2)
        val textToken = view.findViewById<TextView>(R.id.textToken)

        viewtest.text = tokenString
        viewtest2.text = tokenString2
        textToken.text = tokenString3

        return view
    }



}