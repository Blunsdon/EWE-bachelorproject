package com.example.controllockbt.repository

import com.example.controllockbt.api.RetrofitInstance
import com.example.controllockbt.model.PostGetFacInfo
import com.example.controllockbt.model.PostLogin
import com.example.controllockbt.model.PostLogout
import com.example.controllockbt.model.PostSendLog
import retrofit2.Response

class Repository {
    suspend fun pushPostLogin(postLogin: PostLogin): Response<PostLogin> {
        return RetrofitInstance.api.pushPostLogin(postLogin)
    }

    suspend fun pushPostLogout(Authorization: String): Response<PostLogout> {
        return RetrofitInstance.api.pushPostLogout(Authorization)
    }

    suspend fun pushPostGetFacInfo(Authorization: String, postGetFacInfo: PostGetFacInfo): Response<PostGetFacInfo> {
        return RetrofitInstance.api.pushPostGetFacInfo(Authorization, postGetFacInfo)
    }

    suspend fun pushPostSendLog(Authorization: String, postSendLog: PostSendLog): Response<PostSendLog> {
        return RetrofitInstance.api.pushPostSendLog(Authorization, postSendLog)
    }
}