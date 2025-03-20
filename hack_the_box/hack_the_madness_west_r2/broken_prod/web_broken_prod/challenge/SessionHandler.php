<?php
class SessionHandler
{
    public function __construct()
    {
        if (!empty($_COOKIE['PHPSESSID'])){
            $this->cookie = $_COOKIE['PHPSESSID'];
            $this->load();
        }
    }

    public function login($username)
    {
        setcookie('PHPSESSID', base64_encode(json_encode([
            'username' => $username
        ])), time()+1333337, '/');
    }

    public function load()
    {
        $this->data = json_decode(base64_decode($this->cookie));
    }

    public function isLoggedIn()
    {
        return !is_null($this->data->username);
    }

    public function isAdmin()
    {
        return $this->data->username === 'admin';
    }

    public function getUsername()
    {
        return $this->data->username;
    }

    public function distroy()
    {
        unset($_COOKIE['PHPSESSID']);
        setcookie('PHPSESSID', '', time() - 3600, '/');
    }
}