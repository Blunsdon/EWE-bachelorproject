package com.example.controllockbt.activities.FacInfo

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.controllockbt.repository.Repository


class FacInfoModelFactory(private val repository: Repository) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return FacInfoViewModel(repository) as T
    }
}