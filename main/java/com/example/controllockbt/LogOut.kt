package com.example.controllockbt

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class LogOut() : ViewModel() {

    var token: String? = ""
    //internal var token: String? = null
    //internal var token = MutableLiveData<String>()
    // set token value
    @JvmName("setToken1")
    fun setToken(item: String?) {
        token = item
    }

    // get token value
    @JvmName("getToken1")
    fun getToken(): String? {

        return token
    }

}



