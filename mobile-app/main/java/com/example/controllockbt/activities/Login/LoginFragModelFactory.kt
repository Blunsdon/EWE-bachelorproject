package com.example.controllockbt.activities.Login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.controllockbt.repository.Repository



class LoginFragModelFactory(private val repository: Repository) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return LoginFragViewModel(repository) as T
    }
}