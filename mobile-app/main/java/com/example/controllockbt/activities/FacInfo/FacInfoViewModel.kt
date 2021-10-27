package com.example.controllockbt.activities.FacInfo

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.controllockbt.model.PostGetFacInfo
import com.example.controllockbt.repository.Repository
import kotlinx.coroutines.launch
import retrofit2.Response

class FacInfoViewModel(private val repository: Repository): ViewModel() {

    val myResponse: MutableLiveData<Response<PostGetFacInfo>> = MutableLiveData()

    fun pushPost(Authorization: String, postGetFacInfo: PostGetFacInfo) {
        viewModelScope.launch {
            val response: Response<PostGetFacInfo> = repository.pushPostGetFacInfo(Authorization, postGetFacInfo)
            myResponse.value = response
        }
    }

}