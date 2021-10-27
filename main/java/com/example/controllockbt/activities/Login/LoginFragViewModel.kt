package com.example.controllockbt.activities.Login

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.controllockbt.model.PostLogin
import com.example.controllockbt.repository.Repository
import kotlinx.coroutines.launch
import retrofit2.Response

class LoginFragViewModel(private val repository: Repository): ViewModel() {

    val myResponse: MutableLiveData<Response<PostLogin>> = MutableLiveData()

    fun pushPost(postLogin: PostLogin) {
        viewModelScope.launch {
            val response: Response<PostLogin> = repository.pushPostLogin(postLogin)
            myResponse.value = response
        }
    }
}