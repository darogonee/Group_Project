function logout() {
    document.cookie = "user=;expires=Thu, 01 Jan 1970 00:00:01 GMT"
    document.location = "/signin"
}