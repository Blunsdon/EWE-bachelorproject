package com.example.controllockbt.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

import com.example.controllockbt.util.Constants.Companion.BASE_URL

object RetrofitInstance {
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: restAPI by lazy {
        retrofit.create(restAPI::class.java)
    }
}