package com.example.controllockbt;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

public class TokenModel {
    private final MutableLiveData<String> token = new MutableLiveData<String>();

    // store token
    public void setData (String item){

        token.setValue(item);
    }

    // retrieve token
    public LiveData<String> getToken(){

        return token;
    }
}
