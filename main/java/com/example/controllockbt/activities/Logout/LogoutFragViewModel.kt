package com.example.controllockbt.activities.Logout

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.controllockbt.model.PostLogout
import com.example.controllockbt.repository.Repository
import kotlinx.coroutines.launch
import retrofit2.Response

class LogoutFragViewModel(private val repository: Repository): ViewModel() {

    val myResponse: MutableLiveData<Response<PostLogout>> = MutableLiveData()

    fun pushPost(Authorization: String) {
        viewModelScope.launch {
            val response: Response<PostLogout> = repository.pushPostLogout(Authorization)
            myResponse.value = response
        }
    }
}