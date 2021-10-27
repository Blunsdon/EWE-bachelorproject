package com.example.controllockbt.api

import com.example.controllockbt.model.PostGetFacInfo
import com.example.controllockbt.model.PostLogin
import com.example.controllockbt.model.PostLogout
import com.example.controllockbt.model.PostSendLog
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

interface restAPI {
    @POST("api/auth/token/login/")
    suspend fun pushPostLogin(
        @Body postLogin: PostLogin
    ): Response<PostLogin>


    @POST("api/auth/token/logout/")
    suspend fun pushPostLogout(
        @Header("Authorization") Authorization: String
    ): Response<PostLogout>

    @POST("rest_api/key_api/")
    suspend fun pushPostGetFacInfo(
        @Header("Authorization") Authorization: String,
        @Body postGetFacInfo: PostGetFacInfo
    ): Response<PostGetFacInfo>

    @POST("rest_api/log_api/")
    suspend fun pushPostSendLog(
        @Header("Authorization") Authorization: String,
        @Body postSendLog: PostSendLog
    ): Response<PostSendLog>
}