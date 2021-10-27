package com.example.controllockbt.model

data class PostLogin (
    val email: String?,
    val password: String?,
    val auth_token: String?
)

//redundant?
data class PostLogout (
    val auth_token: String?
        )

data class PostGetFacInfo (
    val userEmail: String?,
    var list : List<List<String>>?,
        )

// Next 3 data classes are for the log API
data class PostSendLog (
    val facility : List<Facility>?,
    val log : List<Log>?,
    val key : String?
        )

data class Facility (
    var name : String?
        )

data class Log (

    var userName : String?,
    var companyName : String?,
    var dateTime : String?,
    var userEmail : String?,
    var facilityName : String?,
    var facilityLocation : String?

)