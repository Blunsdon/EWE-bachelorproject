package com.example.controllockbt.activities.SendLog

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.controllockbt.model.PostSendLog
import com.example.controllockbt.repository.Repository
import kotlinx.coroutines.launch
import retrofit2.Response


class SendLogViewModel(private val repository: Repository): ViewModel() {

    val myResponse: MutableLiveData<Response<PostSendLog>> = MutableLiveData()

    fun pushPost(Authorization: String, postSendLog: PostSendLog) {
        viewModelScope.launch {
            val response: Response<PostSendLog> = repository.pushPostSendLog(Authorization, postSendLog)
            myResponse.value = response
        }
    }

}