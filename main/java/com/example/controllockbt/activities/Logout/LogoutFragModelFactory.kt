package com.example.controllockbt.activities.Logout

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.controllockbt.repository.Repository

class LogoutFragModelFactory(private val repository: Repository) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return LogoutFragViewModel(repository) as T
    }
}