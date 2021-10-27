package com.example.controllockbt.activities.SendLog

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.controllockbt.repository.Repository


class SendLogModelFactory(private val repository: Repository) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return SendLogViewModel(repository) as T
    }
}